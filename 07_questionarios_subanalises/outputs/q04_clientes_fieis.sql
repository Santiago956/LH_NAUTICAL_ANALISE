-- Questao 4 - Analise de clientes fieis
-- Banco esperado: PostgreSQL com os CSVs ja carregados.
--
-- Regras:
-- Faturamento Total = SUM(orders.total) por cliente
-- Frequencia = COUNT(DISTINCT orders.id) por cliente
-- Ticket Medio = Faturamento Total / Frequencia
-- Diversidade de Categorias = COUNT(DISTINCT products.category_id)
-- Elite = clientes com diversidade >= 13 categorias
-- Desempate = customer_id em ordem crescente

WITH
metricas_cliente AS (
    SELECT
        o.customer_id,
        SUM(o.total) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia,
        SUM(o.total) / COUNT(DISTINCT o.id) AS ticket_medio
    FROM orders o
    GROUP BY o.customer_id
),

diversidade_cliente AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    INNER JOIN order_items oi
        ON oi.order_id = o.id
    INNER JOIN product_variants pv
        ON pv.id = oi.product_variant_id
    INNER JOIN products p
        ON p.id = pv.product_id
    GROUP BY o.customer_id
),

clientes_fieis AS (
    SELECT
        mc.customer_id,
        mc.faturamento_total,
        mc.frequencia,
        mc.ticket_medio,
        dc.diversidade_categorias
    FROM metricas_cliente mc
    INNER JOIN diversidade_cliente dc
        ON dc.customer_id = mc.customer_id
    WHERE dc.diversidade_categorias >= 13
    ORDER BY
        mc.ticket_medio DESC,
        mc.customer_id ASC
    LIMIT 10
)

SELECT
    customer_id,
    faturamento_total,
    frequencia,
    ticket_medio,
    diversidade_categorias
FROM clientes_fieis
ORDER BY
    ticket_medio DESC,
    customer_id ASC;


-- Categoria mais comprada, em quantidade de itens, pelo grupo dos 10 clientes fieis.

WITH
metricas_cliente AS (
    SELECT
        o.customer_id,
        SUM(o.total) AS faturamento_total,
        COUNT(DISTINCT o.id) AS frequencia,
        SUM(o.total) / COUNT(DISTINCT o.id) AS ticket_medio
    FROM orders o
    GROUP BY o.customer_id
),

diversidade_cliente AS (
    SELECT
        o.customer_id,
        COUNT(DISTINCT p.category_id) AS diversidade_categorias
    FROM orders o
    INNER JOIN order_items oi
        ON oi.order_id = o.id
    INNER JOIN product_variants pv
        ON pv.id = oi.product_variant_id
    INNER JOIN products p
        ON p.id = pv.product_id
    GROUP BY o.customer_id
),

clientes_fieis AS (
    SELECT
        mc.customer_id,
        mc.faturamento_total,
        mc.frequencia,
        mc.ticket_medio,
        dc.diversidade_categorias
    FROM metricas_cliente mc
    INNER JOIN diversidade_cliente dc
        ON dc.customer_id = mc.customer_id
    WHERE dc.diversidade_categorias >= 13
    ORDER BY
        mc.ticket_medio DESC,
        mc.customer_id ASC
    LIMIT 10
)

SELECT
    p.category_id,
    c.name AS categoria,
    SUM(oi.quantity) AS quantidade_total_itens
FROM clientes_fieis cf
INNER JOIN orders o
    ON o.customer_id = cf.customer_id
INNER JOIN order_items oi
    ON oi.order_id = o.id
INNER JOIN product_variants pv
    ON pv.id = oi.product_variant_id
INNER JOIN products p
    ON p.id = pv.product_id
LEFT JOIN categories c
    ON c.id = p.category_id
GROUP BY
    p.category_id,
    c.name
ORDER BY
    quantidade_total_itens DESC,
    p.category_id ASC
LIMIT 1;
