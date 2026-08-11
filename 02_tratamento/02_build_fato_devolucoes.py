import duckdb
import time

print("Iniciando a construção da Fato de Devoluções...")
start_time = time.time()

con = duckdb.connect()

# Query SQL otimizada: Cruza os arquivos brutos de devolução com a base tratada de vendas (Parquet)
query = """
COPY (
    SELECT 
        r.id AS return_id,
        r.order_id,
        CASE 
            WHEN UPPER(r.reason) LIKE '%DUPLICADA%' THEN 'Compra Duplicada'
            WHEN UPPER(r.reason) LIKE '%DEFEITO%' THEN 'Defeito de Fábrica'
            WHEN UPPER(r.reason) LIKE '%DESCRI%' THEN 'Divergência de Descrição'
            WHEN UPPER(r.reason) LIKE '%TAMANHO%' OR UPPER(r.reason) LIKE '%COR%' THEN 'Tamanho/Cor Incorretos'
            WHEN UPPER(r.reason) LIKE '%TRANSPORTE%' OR UPPER(r.reason) LIKE '%AVARIADO%' OR UPPER(r.reason) LIKE '%VARIADO%' THEN 'Avariado no Transporte'
            WHEN UPPER(r.reason) LIKE '%DESISTI%' OR UPPER(r.reason) LIKE '%DESISTU%' THEN 'Desistência'
            ELSE 'Outros'
        END AS return_reason,
        r.created_at AS return_date,
        r.status AS return_status,
        
        ri.order_item_id,
        ri.quantity AS return_quantity,
        ri.action AS return_action,
        (ri.quantity * ri.unit_refund_amount) AS item_refund_total,
        
        fv.product_name,
        fv.sku,
        fv.category_id,
        fv.unit_cost,
        fv.gross_margin AS original_gross_margin
        
    FROM read_csv_auto('data/raw/returns.csv') r
    JOIN read_csv_auto('data/raw/return_items.csv') ri ON r.id = ri.return_id
    -- Usamos o Parquet para herdar os nomes dos produtos e garantir que não traremos vendas "do futuro"
    JOIN 'data/processed/fato_vendas.parquet' fv ON ri.order_item_id = fv.order_item_id
    
    -- TRATAMENTO TEMPORAL (Data Leakage)
    WHERE r.created_at <= '2026-08-10 23:59:59'
) TO 'data/processed/fato_devolucoes.parquet' (FORMAT PARQUET);
"""

try:
    con.execute(query)
    elapsed = time.time() - start_time
    print(f"Sucesso! Fato de Devoluções gerada em data/processed/fato_devolucoes.parquet em {elapsed:.2f} segundos.")
except Exception as e:
    print(f"Erro ao gerar Fato de Devoluções: {e}")
