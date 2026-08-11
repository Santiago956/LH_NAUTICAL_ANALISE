import duckdb
import os
import time

print("Iniciando a construção da Fato de Vendas...")
start_time = time.time()

# Conecta ao DuckDB em memória
con = duckdb.connect()

# Query SQL para Join, Tratamento e Exportação direta para Parquet
# - Faz o JOIN das tabelas raw
# - Remove os dados com "data_leakage" (pedidos pós 2026-08-10)
# - Calcula métricas financeiras essenciais no nível do item (Gross Margin)

query = """
COPY (
    SELECT 
        -- Informações do Pedido
        o.id AS order_id,
        o.placed_at,
        o.status AS order_status,
        o.channel,
        o.location_id,
        
        -- Informações do Item do Pedido
        oi.id AS order_item_id,
        oi.quantity,
        oi.unit_price,
        oi.line_total AS item_revenue,
        
        -- Informações de Custo e Margem (Regras de Negócio)
        pv.cost_price AS unit_cost,
        (oi.quantity * pv.cost_price) AS total_cost,
        (oi.line_total - (oi.quantity * pv.cost_price)) AS gross_margin,
        
        -- Informações de Produto (SKU)
        pv.sku,
        p.name AS product_name,
        p.category_id,
        
        -- Informações de Cliente
        c.id AS customer_id,
        c.person_type,
        
        -- Informações da Localidade
        l.state AS location_state,
        l.city AS location_city
        
    FROM read_csv_auto('data/raw/orders.csv') o
    JOIN read_csv_auto('data/raw/order_items.csv') oi ON o.id = oi.order_id
    JOIN read_csv_auto('data/raw/product_variants.csv') pv ON oi.product_variant_id = pv.id
    JOIN read_csv_auto('data/raw/products.csv') p ON pv.product_id = p.id
    JOIN read_csv_auto('data/raw/customers.csv') c ON o.customer_id = c.id
    LEFT JOIN read_csv_auto('data/raw/locations.csv') l ON o.location_id = l.id
    
    -- TRATAMENTO TEMPORAL (Removendo "Data Leakage" do Futuro)
    WHERE o.placed_at <= '2026-08-10 23:59:59'
) TO 'data/processed/fato_vendas.parquet' (FORMAT PARQUET);
"""

try:
    con.execute(query)
    elapsed = time.time() - start_time
    print(f"Sucesso! Tabela Fato de Vendas gerada em data/processed/fato_vendas.parquet em {elapsed:.2f} segundos.")
except Exception as e:
    print(f"Erro ao gerar Fato de Vendas: {e}")
