
-- 1. Procédure pour nettoyer une session d'examen efficacement
-- Utilise une transaction pour garantir l'intégrité
CREATE OR REPLACE FUNCTION nettoyer_session(p_periode_id INT) 
RETURNS INTEGER AS $$
DECLARE
    v_count INTEGER;
BEGIN
    -- Supprimer d'abord les surveillances liées (contrainte FK)
    DELETE FROM surveillances 
    WHERE examen_id IN (SELECT id FROM examens WHERE periode_id = p_periode_id);
    
    -- Supprimer les examens
    DELETE FROM examens 
    WHERE periode_id = p_periode_id;
    
    GET DIAGNOSTICS v_count = ROW_COUNT;
    
    -- Réinitialiser les statistiques (si on avait une table de cache)
    -- Log l'action (simulation)
    RAISE NOTICE 'Session % nettoyée. % examens supprimés.', p_periode_id, v_count;
    
    RETURN v_count;
END;
$$ LANGUAGE plpgsql;

-- 2. Fonction d'analyse de conflits optimisée (côté serveur)
CREATE OR REPLACE FUNCTION analyser_conflits_etudiants(p_seuil INT DEFAULT 1)
RETURNS TABLE (
    etudiant_nom TEXT,
    date_jour DATE,
    nb_examens BIGINT
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        (e.nom || ' ' || e.prenom)::TEXT,
        DATE(ex.date_heure),
        COUNT(*)
    FROM inscriptions i
    JOIN examens ex ON ex.module_id = i.module_id
    JOIN etudiants e ON e.id = i.etudiant_id
    GROUP BY e.id, e.nom, e.prenom, DATE(ex.date_heure)
    HAVING COUNT(*) > p_seuil
    ORDER BY COUNT(*) DESC;
END;
$$ LANGUAGE plpgsql;
