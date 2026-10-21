SELECT
    priorite,
    COUNT(*) AS tickets,
    ROUND(AVG(duree_h), 1) AS mttr_h,
    ROUND(100 * AVG(sla_respecte::INT), 1) AS respect_sla_pct
FROM tickets
GROUP BY priorite
ORDER BY respect_sla_pct;