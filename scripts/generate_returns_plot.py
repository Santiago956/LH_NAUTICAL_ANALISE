import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme(style="whitegrid")
con = duckdb.connect()

docs_dir = r"E:\repo\lh_nautical_analise\docs"
fato_devolucoes = r"E:\repo\lh_nautical_analise\data\processed\fato_devolucoes.parquet"
plot_path = os.path.join(docs_dir, 'plot_devolucoes.png')

df_ret = con.execute(f"""
    SELECT return_reason as motivo, SUM(item_refund_total) as valor_estornado
    FROM read_parquet('{fato_devolucoes}')
    GROUP BY 1 ORDER BY 2 ASC
""").df()

plt.figure(figsize=(8, 4))
plt.barh(df_ret['motivo'], df_ret['valor_estornado'], color='#d62728')
plt.title('Impacto Financeiro por Motivo de Devolução')
plt.xlabel('Valor Estornado (R$)')
plt.tight_layout()
plt.savefig(plot_path, dpi=150)
plt.close()

print("Gráfico de devoluções gerado com sucesso.")
