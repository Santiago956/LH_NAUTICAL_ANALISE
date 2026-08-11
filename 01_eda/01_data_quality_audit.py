import duckdb
import os
import glob

data_dir = r"E:\repo\lh_nautical_analise\data\raw"

# Conexão em memória (DuckDB é excelente para ler CSVs sem estourar a RAM)
con = duckdb.connect()

print("# Auditoria de Qualidade de Dados (Inicial)\n")

# 1. Contagem de Linhas por Arquivo
print("## 1. Volume de Dados (Linhas por Arquivo)")
files = glob.glob(os.path.join(data_dir, "*.csv"))
for f in files:
    table_name = os.path.basename(f).replace(".csv", "")
    try:
        # A função read_csv_auto do DuckDB infere tipos e carrega o CSV
        count = con.execute(f"SELECT COUNT(*) FROM read_csv_auto('{f}')").fetchone()[0]
        print(f"- **{table_name}**: {count:,} linhas")
    except Exception as e:
        print(f"- **{table_name}**: Erro ao ler ({e})")

# 2. Verificação de Chaves Primárias Duplicadas em Tabelas Centrais
print("\n## 2. Duplicidade em Chaves Primárias (PKs)")
tables_to_check = ['orders', 'customers', 'products', 'product_variants', 'locations']
for t in tables_to_check:
    f = os.path.join(data_dir, f"{t}.csv")
    try:
        dup_count = con.execute(f"""
            SELECT COUNT(*) FROM (
                SELECT id, COUNT(*) as cnt 
                FROM read_csv_auto('{f}') 
                GROUP BY id 
                HAVING cnt > 1
            )
        """).fetchone()[0]
        print(f"- **{t}.id**: {dup_count} IDs duplicados")
    except Exception as e:
        pass

# 3. Anomalias em Pedidos (Datas e Valores Financeiros)
print("\n## 3. Anomalias em Vendas (orders.csv)")
orders_file = os.path.join(data_dir, "orders.csv")
res = con.execute(f"""
    SELECT 
        MIN(placed_at) as min_date,
        MAX(placed_at) as max_date,
        COUNT(*) FILTER (WHERE total < 0) as negative_totals,
        COUNT(*) FILTER (WHERE discount_amount < 0) as negative_discounts,
        COUNT(*) FILTER (WHERE subtotal < 0) as negative_subtotals,
        COUNT(*) FILTER (WHERE status IS NULL) as null_status
    FROM read_csv_auto('{orders_file}')
""").df()

print(f"- **Período dos Pedidos (placed_at):** {res['min_date'][0]} até {res['max_date'][0]}")
print(f"- **Pedidos com Total Negativo:** {res['negative_totals'][0]}")
print(f"- **Pedidos com Desconto Negativo:** {res['negative_discounts'][0]}")
print(f"- **Pedidos com Subtotal Negativo:** {res['negative_subtotals'][0]}")
print(f"- **Pedidos sem Status definido:** {res['null_status'][0]}")

# 4. Anomalias no Catálogo de Produtos
print("\n## 4. Anomalias no Catálogo (product_variants.csv)")
variants_file = os.path.join(data_dir, "product_variants.csv")
res_var = con.execute(f"""
    SELECT 
        COUNT(*) FILTER (WHERE sale_price < cost_price) as prejuizo_na_venda,
        COUNT(*) FILTER (WHERE sale_price <= 0) as preco_zerado_negativo,
        COUNT(*) FILTER (WHERE weight_kg < 0) as peso_negativo
    FROM read_csv_auto('{variants_file}')
""").df()

print(f"- **Variantes onde Preço de Venda < Custo (Prejuízo na Margem Base):** {res_var['prejuizo_na_venda'][0]}")
print(f"- **Variantes com Preço zerado ou negativo:** {res_var['preco_zerado_negativo'][0]}")
print(f"- **Variantes com Peso negativo:** {res_var['peso_negativo'][0]}")
