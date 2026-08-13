import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
con = duckdb.connect()

docs_dir = r"E:\repo\lh_nautical_analise\docs"
fato_vendas = r"E:\repo\lh_nautical_analise\data\processed\fato_vendas.parquet"
categories_raw = r"E:\repo\lh_nautical_analise\data\raw\categories.csv"

# 1. Canais de Venda
df_channel = con.execute(f"""
    SELECT channel, SUM(item_revenue) as receita 
    FROM read_parquet('{fato_vendas}') 
    GROUP BY 1 ORDER BY 2 DESC
""").df()

plt.figure(figsize=(6, 4))
colors = sns.color_palette("pastel")[0:len(df_channel)]
plt.pie(df_channel['receita'], labels=df_channel['channel'].str.title(), autopct='%1.1f%%', colors=colors)
plt.title('Receita por Canal (E-commerce vs Físico)', pad=15)
plt.tight_layout()
plt.savefig(os.path.join(docs_dir, 'plot_canais.png'), dpi=150)
plt.close()

# 2. Categorias Mais Vendidas
df_cat = con.execute(f"""
    SELECT c.name as categoria, SUM(f.item_revenue) as receita
    FROM read_parquet('{fato_vendas}') f
    LEFT JOIN read_csv_auto('{categories_raw}') c ON f.category_id = c.id
    GROUP BY 1 ORDER BY 2 ASC LIMIT 10
""").df()

plt.figure(figsize=(8, 4))
plt.barh(df_cat['categoria'].fillna('Desconhecida'), df_cat['receita'], color='#2ca02c')
plt.title('Top 10 Categorias por Receita')
plt.xlabel('Receita Total (R$)')
plt.tight_layout()
plt.savefig(os.path.join(docs_dir, 'plot_categorias.png'), dpi=150)
plt.close()

print("Novos gráficos gerados com sucesso.")
