import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import os

sns.set_theme(style="whitegrid")
con = duckdb.connect()

# Output paths
docs_dir = r"E:\repo\lh_nautical_analise\docs"
os.makedirs(docs_dir, exist_ok=True)
plot1_path = os.path.join(docs_dir, "plot_seasonality.png")
plot2_path = os.path.join(docs_dir, "plot_pareto.png")

# 1. Generate Seasonality Plot
df_ts = con.execute("""
    SELECT DATE_TRUNC('month', placed_at) as mes, SUM(total) as receita
    FROM read_csv_auto('E:/repo/lh_nautical_analise/data/raw/orders.csv')
    WHERE placed_at >= '2020-01-01' AND placed_at < '2026-08-01'
    GROUP BY 1 ORDER BY 1
""").df()
df_ts['mes'] = pd.to_datetime(df_ts['mes'])

plt.figure(figsize=(10, 4))
plt.plot(df_ts['mes'], df_ts['receita'], color='#1f77b4', linewidth=2)
plt.title('Receita Mensal: Forte Sazonalidade de Verão', fontsize=14, pad=15)
plt.ylabel('Receita (R$)')
plt.xlabel('Ano')
plt.tight_layout()
plt.savefig(plot1_path, dpi=150)
plt.close()

# 2. Generate Pareto Plot
df_clientes = con.execute("""
    SELECT id as customer_id, SUM(receita_total) as receita_total
    FROM read_parquet('E:/repo/lh_nautical_analise/data/processed/dim_clientes.parquet')
    WHERE receita_total > 0
    GROUP BY 1 ORDER BY 2 DESC
""").df()
df_clientes['receita_acumulada'] = df_clientes['receita_total'].cumsum()
df_clientes['perc_receita_acumulada'] = df_clientes['receita_acumulada'] / df_clientes['receita_total'].sum()
df_clientes['perc_clientes'] = np.arange(1, len(df_clientes) + 1) / len(df_clientes)

plt.figure(figsize=(8, 4))
plt.plot(df_clientes['perc_clientes'] * 100, df_clientes['perc_receita_acumulada'] * 100, color='#ff7f0e', linewidth=2)
plt.axvline(x=71.6, color='red', linestyle='--', alpha=0.7)
plt.axhline(y=80, color='red', linestyle='--', alpha=0.7)
plt.scatter([71.6], [80], color='red', zorder=5)
plt.title('Curva de Concentração de Receita (Ausência de Pareto)', fontsize=14, pad=15)
plt.xlabel('% de Clientes')
plt.ylabel('% da Receita Acumulada')
plt.tight_layout()
plt.savefig(plot2_path, dpi=150)
plt.close()

# 3. Create PDF
class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', 'B', 15)
        self.cell(0, 10, 'LH Nautical - Sumário Executivo de Negócios', 0, 1, 'C')
        self.set_font('helvetica', 'I', 10)
        self.cell(0, 10, 'Inteligência de Dados | Foco em Rentabilidade e Expansão', 0, 1, 'C')
        self.ln(5)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('helvetica', 'B', 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, f' {title}', 0, 1, 'L', 1)
        self.ln(4)

    def chapter_body(self, text):
        self.set_font('helvetica', '', 11)
        self.multi_cell(0, 6, text)
        self.ln(4)
        
    def fhr_block(self, fato, hipotese, recomendacao):
        self.set_font('helvetica', 'B', 10)
        self.multi_cell(0, 6, 'Fato: ' + fato)
        self.multi_cell(0, 6, 'Hipótese: ' + hipotese)
        self.multi_cell(0, 6, 'Recomendação: ' + recomendacao)
        self.ln(6)

pdf = PDF()
pdf.add_page()

# Intro
pdf.set_font('helvetica', '', 11)
intro = "Este relatório sintetiza os achados da auditoria e modelagem de dados da LH Nautical (2020-2026), focando em alavancas de lucro, falhas operacionais e previsão de demanda."
pdf.multi_cell(0, 6, intro)
pdf.ln(5)

# Chapter 1
pdf.chapter_title('1. Rentabilidade e Ralo Logístico (Devoluções)')
pdf.fhr_block(
    "Os Top produtos possuem margem bruta saudável (>50%). Não há ofensores graves de margem na precificação de ponta.",
    "A política de descontos está bem calibrada pela área comercial.",
    "Manter a estratégia atual de preços e descontos."
)
pdf.fhr_block(
    "Identificamos severo prejuízo logístico através das devoluções. Principais motivos: Desistências, Tamanho Errado e Avarias.",
    "Temos dois gargalos simultâneos: Fricção Digital (interface pobre no E-commerce) e Fricção Física (transporte descuidado/avarias).",
    "Acionar UX/UI para melhorar a página de produtos (tabela de medidas) e iniciar auditoria com as transportadoras sobre avarias."
)

# Chapter 2
pdf.chapter_title('2. Perfil de Clientes e Clusterização')
pdf.image(plot2_path, w=150)
pdf.fhr_block(
    "A receita da companhia é extremamente pulverizada. São necessários 71,6% dos clientes para compor 80% do faturamento.",
    "O perfil da LH Nautical é massivamente B2C (consumidor final), sem dependência de 'Baleias' (grandes atacadistas/B2B).",
    "Descartar estratégias VIP (Key Account Management). Investir pesado em escala e automação de CRM."
)

pdf.add_page()
# Chapter 3
pdf.chapter_title('3. Previsão de Demanda e Estoque')
pdf.image(plot1_path, w=160)
pdf.fhr_block(
    "Crescimento orgânico contínuo (YOY) com sazonalidade extrema: Picos no Verão (Dezembro a Fevereiro).",
    "Os consumidores antecipam e realizam compras concentradas para as férias e festas de fim de ano.",
    "A área de Suprimentos deve emitir Purchase Orders IMEDIATAMENTE (Ago/Set) para cobrir a alta demanda projetada para Nov/Dez. Sem isso, ocorrerá ruptura de estoque."
)

# Chapter 4
pdf.chapter_title('4. Ações de Crescimento (Cross-Sell)')
pdf.fhr_block(
    "Através de Matriz de Co-ocorrência em SQL (Market Basket Analysis), mapeamos milhares de regras de associação orgânicas ('Quem comprou X, levou Y').",
    "Como a base é puramente B2C e fragmentada, sugerir itens complementares é a alavanca mais barata e rápida para aumentar o Ticket Médio.",
    "Implantar o modelo de recomendação construído na Etapa 06 diretamente no carrinho do E-commerce e nas campanhas de e-mail marketing."
)

pdf_output = os.path.join(docs_dir, "EXECUTIVE_SUMMARY.pdf")
pdf.output(pdf_output)
print(f"PDF gerado com sucesso em: {pdf_output}")
