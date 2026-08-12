import duckdb
import os

def build_dim_clientes():
    print("Construindo dimensão consolidada de clientes...")
    
    con = duckdb.connect()
    raw_dir = r"E:\repo\lh_nautical_analise\data\raw"
    proc_dir = r"E:\repo\lh_nautical_analise\data\processed"
    os.makedirs(proc_dir, exist_ok=True)
    
    # Cruzando clientes com endereços e criando um resumo de pedidos por cliente
    query = f"""
    CREATE OR REPLACE TABLE dim_clientes AS 
    WITH pedidos_resumo AS (
        SELECT 
            customer_id,
            COUNT(id) as total_pedidos,
            MIN(placed_at) as data_primeira_compra,
            MAX(placed_at) as data_ultima_compra,
            SUM(total) as receita_total,
            SUM(discount_amount) as total_descontos
        FROM read_csv_auto('{raw_dir}/orders.csv')
        WHERE placed_at <= '2026-08-10' -- Truncamento temporal (Data Leakage Protection)
        GROUP BY customer_id
    )
    SELECT 
        c.*,
        a.street,
        a.city,
        a.state,
        a.postal_code,
        a.country,
        COALESCE(p.total_pedidos, 0) as total_pedidos,
        p.data_primeira_compra,
        p.data_ultima_compra,
        COALESCE(p.receita_total, 0) as receita_total,
        COALESCE(p.total_descontos, 0) as total_descontos
    FROM read_csv_auto('{raw_dir}/customers.csv') c
    LEFT JOIN read_csv_auto('{raw_dir}/addresses.csv') a ON c.id = a.customer_id
    LEFT JOIN pedidos_resumo p ON c.id = p.customer_id
    """
    
    con.execute(query)
    
    out_path = os.path.join(proc_dir, "dim_clientes.parquet")
    con.execute(f"COPY dim_clientes TO '{out_path}' (FORMAT PARQUET)")
    
    print(f"Dimensão de Clientes (Customer 360) criada com sucesso: {out_path}")
    
if __name__ == "__main__":
    build_dim_clientes()
