-- Questao 1 - EDA
-- Tabela utilizada: orders
-- Objetivo: observar volume, periodo, estatisticas basicas de total
-- e sinais iniciais de qualidade sem limpar ou tratar os dados.

SELECT
    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima_created_at,
    MAX(created_at) AS data_maxima_created_at,
    MIN(total) AS valor_minimo_total,
    MAX(total) AS valor_maximo_total,
    AVG(total) AS valor_medio_total,
    SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END) AS created_at_nulos,
    SUM(CASE WHEN total IS NULL THEN 1 ELSE 0 END) AS total_nulos,
    SUM(CASE WHEN total < 0 THEN 1 ELSE 0 END) AS total_negativo,
    SUM(CASE WHEN total = 0 THEN 1 ELSE 0 END) AS total_zero
FROM orders;
