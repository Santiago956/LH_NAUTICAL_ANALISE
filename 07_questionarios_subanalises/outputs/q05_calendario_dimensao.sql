-- Questao 5 - Dimensao de calendario
-- Banco esperado: PostgreSQL com os CSVs ja carregados (schema da Questao 2).
--
-- Premissas:
-- 1. Periodo: todas as datas entre o menor e o maior created_at de vendas no arquivo.
-- 2. A loja esteve aberta em todos os dias do periodo (inclusive fins de semana).
-- 3. Apenas lojas fisicas: channel = 'pos'.
-- 4. Dias sem registro de venda entram como valor 0.
-- 5. Vendas diarias = SUM(total) por dia.
-- 6. A media por dia da semana considera todos os dias do calendario.
-- 7. Nome do dia da semana em portugues.
--
-- OBS: used_at == placed_at em 100% das linhas de orders (validado nos CSVs),
-- portanto a data da venda e indiferente entre as duas colunas.

-- =============================================================
-- 1) DIMENSAO DE DATAS (calendario)
--    Gera uma linha por dia, de 2020-01-01 ate 2026-12-31
--    (menor e maior data de venda presentes em orders).
-- =============================================================
CREATE TABLE IF NOT EXISTS dim_data AS
SELECT
    data::date                                             AS data,
    EXTRACT(DOW FROM data)::int                            AS numero_dia_semana,
    CASE EXTRACT(DOW FROM data)
        WHEN 0 THEN 'Domingo'
        WHEN 1 THEN 'Segunda-feira'
        WHEN 2 THEN 'Terca-feira'
        WHEN 3 THEN 'Quarta-feira'
        WHEN 4 THEN 'Quinta-feira'
        WHEN 5 THEN 'Sexta-feira'
        WHEN 6 THEN 'Sabado'
    END                                                    AS dia_semana
FROM generate_series(
    (SELECT MIN(created_at)::date FROM orders),
    (SELECT MAX(created_at)::date FROM orders),
    INTERVAL '1 day'
) AS data(data);

-- =============================================================
-- 2) VENDAS DIARIAS (apenas lojas fisicas)
--    Soma do valor da venda (orders.total) por dia.
-- =============================================================
CREATE TABLE IF NOT EXISTS vendas_diarias_pos AS
SELECT
    created_at::date AS data,
    SUM(total)       AS valor_venda
FROM orders
WHERE channel = 'pos'
GROUP BY created_at::date;

-- =============================================================
-- 3) CRUZAMENTO CALENDARIO x VENDAS
--    LEFT JOIN garante que todos os dias do calendario aparecam;
--    dias sem venda recebem 0 via COALESCE.
-- =============================================================
CREATE TABLE IF NOT EXISTS calendario_vendas AS
SELECT
    d.data,
    d.numero_dia_semana,
    d.dia_semana,
    COALESCE(v.valor_venda, 0) AS valor_venda
FROM dim_data d
LEFT JOIN vendas_diarias_pos v
    ON v.data = d.data;

-- =============================================================
-- 4) RESPOSTA: media de vendas por dia da semana
--    A media usa todos os dias do calendario (inclusive dias = 0),
--    por isso NAO e inflada por dias que abriram e venderam zero.
-- =============================================================
SELECT
    dia_semana,
    numero_dia_semana,
    COUNT(*)                                      AS dias_no_periodo,
    SUM(CASE WHEN valor_venda = 0 THEN 1 ELSE 0 END) AS dias_sem_venda,
    SUM(valor_venda)                              AS vendas_totais,
    ROUND(AVG(valor_venda), 2)                    AS media_vendas_por_dia
FROM calendario_vendas
GROUP BY dia_semana, numero_dia_semana
ORDER BY media_vendas_por_dia ASC, numero_dia_semana ASC;

-- =============================================================
-- 5) VARIANTE EM QUERY UNICA (CTE), sem criar tabelas
--    Util para conferencia rapida e para ambientes sem DDL.
-- =============================================================
WITH RECURSIVE
calendario AS (
    SELECT (SELECT MIN(created_at)::date FROM orders) AS data
    UNION ALL
    SELECT data + INTERVAL '1 day'
    FROM calendario
    WHERE data < (SELECT MAX(created_at)::date FROM orders)
),
vendas_por_dia AS (
    SELECT
        created_at::date AS data,
        SUM(total)       AS valor_venda
    FROM orders
    WHERE channel = 'pos'
    GROUP BY created_at::date
),
vendas_diarias AS (
    SELECT
        c.data,
        CASE EXTRACT(DOW FROM c.data)
            WHEN 0 THEN 'Domingo'
            WHEN 1 THEN 'Segunda-feira'
            WHEN 2 THEN 'Terca-feira'
            WHEN 3 THEN 'Quarta-feira'
            WHEN 4 THEN 'Quinta-feira'
            WHEN 5 THEN 'Sexta-feira'
            WHEN 6 THEN 'Sabado'
        END                AS dia_semana,
        COALESCE(v.valor_venda, 0) AS valor_venda
    FROM calendario c
    LEFT JOIN vendas_por_dia v
        ON v.data = c.data
)
SELECT
    dia_semana,
    COUNT(*)                                       AS dias_no_periodo,
    SUM(CASE WHEN valor_venda = 0 THEN 1 ELSE 0 END) AS dias_sem_venda,
    SUM(valor_venda)                               AS vendas_totais,
    ROUND(AVG(valor_venda), 2)                     AS media_vendas_por_dia
FROM vendas_diarias
GROUP BY dia_semana
ORDER BY media_vendas_por_dia ASC;