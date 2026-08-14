import pandas as pd
import duckdb
import os

def main():
    base_dir = 'data/processed'
    
    # 1. Convert Parquet to CSV
    files_to_convert = [
        'fato_vendas.parquet',
        'fato_devolucoes.parquet',
        'dim_clientes.parquet'
    ]
    
    for file in files_to_convert:
        in_path = os.path.join(base_dir, file)
        out_name = file.replace('.parquet', '_looker.csv')
        out_path = os.path.join(base_dir, out_name)
        
        if os.path.exists(in_path):
            print(f"Lendo {in_path}...")
            df = pd.read_parquet(in_path)
            print(f"Exportando para {out_path}...")
            df.to_csv(out_path, index=False, encoding='utf-8')
        else:
            print(f"Aviso: {in_path} não encontrado.")
            
    # 2. Gerar base da Questão 5 (Dias da semana zerados)
    conn = duckdb.connect()
    sql_q5 = """
    WITH RECURSIVE calendario AS (
        SELECT (SELECT MIN(created_at)::date FROM read_csv_auto('data/raw/orders.csv')) AS data
        UNION ALL
        SELECT data + INTERVAL '1 day'
        FROM calendario
        WHERE data < (SELECT MAX(created_at)::date FROM read_csv_auto('data/raw/orders.csv'))
    ),
    vendas_por_dia AS (
        SELECT
            created_at::date AS data,
            SUM(total)       AS valor_venda
        FROM read_csv_auto('data/raw/orders.csv')
        WHERE channel = 'pos'
        GROUP BY created_at::date
    ),
    vendas_diarias AS (
        SELECT
            c.data,
            CASE EXTRACT(DOW FROM c.data)
                WHEN 0 THEN 'Domingo'
                WHEN 1 THEN 'Segunda-feira'
                WHEN 2 THEN 'Terça-feira'
                WHEN 3 THEN 'Quarta-feira'
                WHEN 4 THEN 'Quinta-feira'
                WHEN 5 THEN 'Sexta-feira'
                WHEN 6 THEN 'Sábado'
            END                AS dia_semana,
            EXTRACT(DOW FROM c.data) AS numero_dia,
            COALESCE(v.valor_venda, 0) AS valor_venda
        FROM calendario c
        LEFT JOIN vendas_por_dia v
            ON v.data = c.data
    )
    SELECT
        dia_semana,
        numero_dia,
        COUNT(*)                                       AS dias_no_periodo,
        SUM(CASE WHEN valor_venda = 0 THEN 1 ELSE 0 END) AS dias_sem_venda,
        ROUND(SUM(valor_venda), 2)                     AS vendas_totais,
        ROUND(AVG(valor_venda), 2)                     AS media_vendas_por_dia
    FROM vendas_diarias
    GROUP BY dia_semana, numero_dia
    ORDER BY numero_dia ASC;
    """
    
    print("Gerando CSV para Questão 5 (Dias da Semana)...")
    df_q5 = conn.execute(sql_q5).df()
    df_q5.to_csv(os.path.join(base_dir, 'q5_dias_semana_looker.csv'), index=False, encoding='utf-8')
    conn.close()
    
    print("Todas as bases CSV foram geradas com sucesso em data/processed!")

if __name__ == '__main__':
    main()
