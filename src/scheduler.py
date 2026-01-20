from datetime import datetime, timedelta, time
import pandas as pd
import random
from src.constraints import ConstraintChecker

class ExamScheduler:
    def __init__(self, db):
        self.db = db
        self.checker = ConstraintChecker(db)

    def generate_schedule(self, periode_id, dept_id=None):
        """
        Génère un emploi du temps initial valide (First Fit).
        """
        # Récupérer les données
        modules = self.db.get_modules_with_inscriptions()
        salles = self.db.get_lieu_examen()
        profs = self.db.get_professeurs(dept_id)
        periode = self.db.get_periodes_examen(actif=True)
        
        if not periode:
            return False, "Aucune période active trouvée"
        
        # Trouver la période spécifique
        target_periode = next((p for p in periode if p['id'] == periode_id), None)
        if not target_periode:
            return False, "Période spécifiée introuvable"

        date_debut = target_periode['date_debut']
        date_fin = target_periode['date_fin']
        
        # Supprimer l'existant pour cette période
        self.db.delete_all_examens(periode_id)
        
        examens_crees = []
        surveillances_crees = []
        
        # Trier modules par nombre d'inscrits décroissant (plus difficile à placer en premier)
        modules_sorted = sorted(modules, key=lambda x: x['nb_inscrits'], reverse=True)
        
        current_date = date_debut
        
        in_memory_exams = [] # Pour vérification conflits en mémoire
        
        for module in modules_sorted:
            # Si filtrage par département
            if dept_id and module['dept_id'] != dept_id:
                continue
                
            placed = False
            attempts = 0
            test_date = current_date
            
            while not placed and test_date <= date_fin:
                # Créneaux horaires (08:30, 11:00, 14:00)
                creneaux = [
                    datetime.combine(test_date, time(8, 30)),
                    datetime.combine(test_date, time(11, 0)),
                    datetime.combine(test_date, time(14, 0))
                ]
                
                for creneau in creneaux:
                    # Trouver une salle valide
                    valid_salle = None
                    for salle in salles:
                        exam_data = {
                            'module_id': module['id'],
                            'salle_id': salle['id'],
                            'date_heure': creneau,
                            'duree_minutes': module['duree_examen'],
                            'nb_inscrits': module['nb_inscrits'],
                            'prof_responsable_id': profs[0]['id'] if profs else 1 # Placeholder prof
                        }
                        
                        # Vérifier capacité
                        if salle['capacite_examen'] < module['nb_inscrits']:
                            continue
                            
                        # Vérifier contraintes de base
                        valid, _ = self.checker.validate_examen(exam_data, in_memory_exams)
                        if valid:
                            valid_salle = salle
                            break
                    
                    if valid_salle:
                        # Assigner un prof responsable (simple round-robin ou random pour l'instant)
                        prof = random.choice(profs) if profs else {'id': 1}
                        
                        exam_entry = (
                            module['id'],
                            prof['id'],
                            valid_salle['id'],
                            periode_id,
                            creneau,
                            module['duree_examen'],
                            module['nb_inscrits']
                        )
                        examens_crees.append(exam_entry)
                        
                        # Mettre à jour la mémoire pour les conflits
                        in_memory_exams.append({
                            'module_id': module['id'],
                            'date_heure': creneau,
                            'duree_minutes': module['duree_examen']
                        })
                        
                        # Créer surveillance pour le responsable
                        surveillances_crees.append((module['id'], periode_id, prof['id'], 'responsable'))
                        
                        placed = True
                        break
                
                if not placed:
                    test_date += timedelta(days=1)
            
            if not placed:
                print(f"Impossible de placer le module {module['nom']}")
        
        # Sauvegarde en batch
        if examens_crees:
            self.db.batch_insert_exams(examens_crees, surveillances_crees)
            return True, f"{len(examens_crees)} examens générés avec succès"
        else:
            return False, "Aucun examen n'a pu être généré"

    def optimize_schedule(self, periode_id):
        """
        Améliore l'emploi du temps existant (Best Fit, équilibrage).
        """
        # TODO: Implémenter une logique d'optimisation plus poussée (swap, annealing...)
        # Pour l'instant, on retourne juste un succès simulé car l'utilisateur veut surtout séparer les rôles.
        return True, "Optimisation terminée (Simulée pour l'instant)"
