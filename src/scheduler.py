import time
from datetime import datetime, timedelta, time as dt_time
import pandas as pd
import random
from collections import defaultdict

class ExamScheduler:
    def __init__(self, db):
        self.db = db

    def generate_schedule(self, periode_id, dept_id=None):
        """
        Génère un emploi du temps initial valide (First Fit) avec optimisation en mémoire.
        """
        start_time = time.time()
        
        # Récupérer les données une seule fois
        modules = self.db.get_modules_with_inscriptions()
        salles = self.db.get_lieu_examen()
        profs = self.db.get_professeurs(dept_id)
        periodes = self.db.get_periodes_examen(actif=True)
        
        if not periodes:
            return False, {"error": "Aucune période active trouvée"}
        
        # Trouver la période spécifique
        target_periode = next((p for p in periodes if p['id'] == periode_id), None)
        if not target_periode:
            return False, {"error": "Période spécifiée introuvable"}

        date_debut = target_periode['date_debut']
        date_fin = target_periode['date_fin']
        
        # Supprimer l'existant pour cette période
        self.db.delete_all_examens(periode_id)
        
        examens_crees = []
        surveillances_crees = []
        
        # Structures de données en mémoire pour validation ultra-rapide
        # (salle_id, datetime) -> True
        salle_occupancy = set()
        
        # (prof_id, datetime) -> True
        prof_occupancy = set()
        
        # (prof_id, date) -> count
        prof_daily_count = defaultdict(int)
        
        # (formation_id, date) -> True (Pour éviter 2 examens le même jour pour la même promo)
        formation_daily_occupancy = defaultdict(set)
        
        # Trier modules par nombre d'inscrits décroissant
        modules_sorted = sorted(modules, key=lambda x: x['nb_inscrits'], reverse=True)
        
        current_date_pointer = date_debut
        
        nb_modules_places = 0
        failed_modules = []
        
        for module in modules_sorted:
            # Si filtrage par département
            if dept_id and module['dept_id'] != dept_id:
                continue
            
            placed = False
            test_date = current_date_pointer
            
            # Limite de recherche pour éviter boucle infinie (date fin + marge)
            max_days_search = (date_fin - date_debut).days + 1
            days_searched = 0
            
            while not placed and test_date <= date_fin:
                # Créneaux horaires (08:30, 11:00, 14:00)
                creneaux = [
                    datetime.combine(test_date, dt_time(8, 30)),
                    datetime.combine(test_date, dt_time(11, 0)),
                    datetime.combine(test_date, dt_time(14, 0))
                ]
                
                module_formation = module['formation_id']
                
                # Vérifier si la formation a déjà un examen ce jour-là
                if test_date in formation_daily_occupancy[module_formation]:
                    # Passer au jour suivant
                    test_date += timedelta(days=1)
                    days_searched += 1
                    continue

                for creneau in creneaux:
                    valid_salle = None
                    
                    for salle in salles:
                        # 1. Vérifier capacité
                        if salle['capacite_examen'] < module['nb_inscrits']:
                            continue
                        
                        # 2. Vérifier disponibilité salle
                        if (salle['id'], creneau) in salle_occupancy:
                            continue
                            
                        # Salle valide trouvée
                        valid_salle = salle
                        break
                    
                    if valid_salle:
                        # Trouver un prof disponible
                        valid_prof = None
                        candidates = profs if profs else [{'id': 1, 'nom': 'N/A', 'prenom': 'N/A'}]
                        
                        # Essayer de trouver un prof libre
                        for prof in candidates:
                            p_id = prof['id']
                            # Vérifier dispo créneau
                            if (p_id, creneau) in prof_occupancy:
                                continue
                            # Vérifier max 3 par jour
                            if prof_daily_count[(p_id, test_date)] >= 3:
                                continue
                                
                            valid_prof = prof
                            break
                        
                        if valid_prof:
                            # Tout est bon, on réserve
                            
                            exam_entry = (
                                module['id'],
                                valid_prof['id'],
                                valid_salle['id'],
                                periode_id,
                                creneau,
                                module['duree_examen'],
                                module['nb_inscrits']
                            )
                            examens_crees.append(exam_entry)
                            
                            # Enregistrer surveillance
                            surveillances_crees.append((module['id'], periode_id, valid_prof['id'], 'responsable'))
                            
                            # Mettre à jour les structures en mémoire
                            salle_occupancy.add((valid_salle['id'], creneau))
                            prof_occupancy.add((valid_prof['id'], creneau))
                            prof_daily_count[(valid_prof['id'], test_date)] += 1
                            formation_daily_occupancy[module_formation].add(test_date)
                            
                            placed = True
                            nb_modules_places += 1
                            break
                
                if not placed:
                    test_date += timedelta(days=1)
                    days_searched += 1
            
            if not placed:
                print(f"Impossible de placer le module {module['nom']} ({module['nb_inscrits']} inscrits)")
                failed_modules.append({'nom': module['nom'], 'inscrits': module['nb_inscrits']})
        
        # Sauvegarde en batch
        if examens_crees:
            self.db.batch_insert_exams(examens_crees, surveillances_crees)
            
            end_time = time.time()
            return True, {
                'execution_time': end_time - start_time,
                'scheduled': len(examens_crees),
                'failed': len(failed_modules),
                'total_conflicts': 0, # In-memory guarantees 0 hard conflicts
                'failed_modules': failed_modules
            }
        else:
            return False, {"error": "Aucun examen n'a pu être généré (peut-être manque de salles/profs ?)"}

    def optimize_schedule(self, periode_id):
        """
        Améliore l'emploi du temps existant (Best Fit, équilibrage).
        """
        # TODO: Implémenter une logique d'optimisation plus poussée (swap, annealing...)
        return True, "Optimisation terminée (Simulée pour l'instant)"
