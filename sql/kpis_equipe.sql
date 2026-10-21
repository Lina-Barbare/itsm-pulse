-- la requete pour afficher la performance de chaque equipe de la pire a la meilleure
SELECT
    equipe,
    COUNT(*) AS tickets,
    ROUND(AVG(duree_h), 1) AS mttr_h,
    ROUND(100 * AVG(sla_respecte::INT), 1) AS respect_sla_pct,
    ROUND(100 * AVG((reouvertures > 0)::INT), 1) AS reouverture_pct
FROM tickets
GROUP BY equipe
ORDER BY respect_sla_pct;