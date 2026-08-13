import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

docs_dir = r"E:\repo\lh_nautical_analise\docs"
pdf_path = os.path.join(docs_dir, "EXECUTIVE_SUMMARY_V2.pdf")
plot1_path = os.path.join(docs_dir, "plot_seasonality.png")
plot2_path = os.path.join(docs_dir, "plot_pareto.png")
plot_canais_path = os.path.join(docs_dir, "plot_canais.png")
plot_categorias_path = os.path.join(docs_dir, "plot_categorias.png")

doc = SimpleDocTemplate(pdf_path, pagesize=letter)
styles = getSampleStyleSheet()

# Custom styles
title_style = styles['Heading1']
title_style.alignment = 1 # Center

h2_style = styles['Heading2']
h2_style.textColor = "blue"

normal_style = styles['Normal']
normal_style.fontSize = 11
normal_style.leading = 14

story = []

story.append(Paragraph("LH Nautical - Sumário Executivo de Negócios", title_style))
story.append(Paragraph("Inteligência de Dados | Foco em Rentabilidade e Expansão", normal_style))
story.append(Spacer(1, 20))

intro = "Este relatório sintetiza os achados da auditoria e modelagem de dados da LH Nautical (2020-2026), focando em performance de vendas, alavancas de lucro, falhas operacionais e previsão de demanda."
story.append(Paragraph(intro, normal_style))
story.append(Spacer(1, 10))

def add_fhr(fato, hipotese, recomendacao):
    story.append(Paragraph(f"<b>Fato Observado:</b> {fato}", normal_style))
    story.append(Paragraph(f"<b>Hipótese:</b> {hipotese}", normal_style))
    story.append(Paragraph(f"<b>Recomendação:</b> {recomendacao}", normal_style))
    story.append(Spacer(1, 12))

# NOVO CAPITULO: Fotografia do Faturamento
story.append(Paragraph("1. Performance: Canais e Categorias", h2_style))
if os.path.exists(plot_canais_path):
    story.append(Image(plot_canais_path, width=300, height=200))
if os.path.exists(plot_categorias_path):
    story.append(Image(plot_categorias_path, width=400, height=200))
add_fhr(
    "A receita da LH Nautical é fortemente ancorada no E-commerce em detrimento das lojas físicas, e as categorias de itens náuticos pesados lideram a receita global.",
    "Apesar das lojas físicas possuírem menor volume financeiro relativo, elas podem estar operando como showrooms ou pontos de assistência.",
    "Avaliar com a área Comercial se o foco de expansão será 100% digital, ou se há interesse em revitalizar as vendas no varejo físico."
)

# Capítulo 2. Rentabilidade e Devoluções
story.append(Paragraph("2. Rentabilidade e Ralo Logístico (Devoluções)", h2_style))
add_fhr(
    "Os Top produtos possuem margem bruta saudável (>50%). Não há ofensores graves de margem na precificação de ponta.",
    "A política de descontos está bem calibrada pela área comercial.",
    "Manter a estratégia atual de preços e descontos."
)
add_fhr(
    "Identificamos severo prejuízo logístico através das devoluções. Principais motivos: Desistências, Tamanho Errado e Avarias no Transporte.",
    "Temos dois gargalos simultâneos: Fricção Digital (interface confusa no E-commerce gerando desistências) e Fricção Física (transporte descuidado/avarias).",
    "Acionar UX/UI para melhorar a página de produtos e iniciar auditoria com as transportadoras sobre quebra de mercadorias."
)

# Capítulo 3. Clientes
story.append(Paragraph("3. Perfil de Clientes e Clusterização", h2_style))
if os.path.exists(plot2_path):
    story.append(Image(plot2_path, width=400, height=200))
add_fhr(
    "A receita da companhia é extremamente pulverizada. São necessários 71,6% dos clientes para compor 80% do faturamento.",
    "O perfil da LH Nautical é massivamente B2C (consumidor final), sem dependência de 'Baleias' (grandes atacadistas/B2B).",
    "Descartar estratégias VIP (Key Account Management). Investir pesado em escala, automação de CRM e motores de recomendação."
)

# Capítulo 4. Demanda
story.append(Paragraph("4. Previsão de Demanda e Estoque", h2_style))
if os.path.exists(plot1_path):
    story.append(Image(plot1_path, width=450, height=180))
add_fhr(
    "Crescimento orgânico contínuo (YOY) com sazonalidade extrema: Picos de venda sempre no Verão (Dezembro a Fevereiro).",
    "Consumidores antecipam e realizam compras concentradas para as férias de verão.",
    "A área de Suprimentos deve emitir Purchase Orders IMEDIATAMENTE (Ago/Set) para cobrir a alta demanda projetada. Sem isso, ocorrerá ruptura de estoque gravíssima."
)

# Capítulo 5. Cross Sell
story.append(Paragraph("5. Ações de Crescimento (Cross-Sell)", h2_style))
add_fhr(
    "Através da construção de uma Matriz de Co-ocorrência, extraímos milhares de regras orgânicas de vendas casadas ('Quem comprou X, levou Y').",
    "Em uma base B2C pulverizada, ferramentas automatizadas de recomendação são a forma mais efetiva de aumentar o Ticket Médio.",
    "Implantar o modelo de recomendação construído na Etapa 06 no carrinho do E-commerce e engatilhar fluxos de e-mail marketing."
)

doc.build(story)
print(f"PDF ATUALIZADO com sucesso em {pdf_path}")
