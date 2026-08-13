import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA E ESTILIZAÇÃO
# ==========================================
st.set_page_config(page_title="LH Nautical | Inteligência Executiva", page_icon="⛵", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Inter', sans-serif;
    }
    
    /* Cards de KPI */
    div[data-testid="stMetricValue"] {
        font-size: 28px !important;
        font-weight: 700 !important;
        color: #0f172a !important; 
    }
    div[data-testid="stMetricLabel"] {
        font-size: 14px !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
    }
    
    div[data-testid="metric-container"] {
        background-color: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 16px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    }
    
    /* Esconder menu do Streamlit para visual mais limpo */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. CARREGAMENTO DE DADOS (PERFORMANCE)
# ==========================================
@st.cache_resource
def get_db_connection():
    return duckdb.connect()

con = get_db_connection()

@st.cache_data
def load_base_data():
    conn = duckdb.connect()
    fato_vendas = "E:/repo/lh_nautical_analise/data/processed/fato_vendas.parquet"
    fato_devolucoes = "E:/repo/lh_nautical_analise/data/processed/fato_devolucoes.parquet"
    categories = "E:/repo/lh_nautical_analise/data/raw/categories.csv"
    
    # Base inteira de vendas em memória (Pandas)
    df_vendas = conn.execute(f"""
        SELECT 
            f.order_id, f.placed_at, f.channel, f.item_revenue, f.gross_margin, 
            f.customer_id, f.sku, f.product_name, c.name as category_name
        FROM read_parquet('{fato_vendas}') f
        LEFT JOIN read_csv_auto('{categories}') c ON f.category_id = c.id
    """).df()
    
    df_dev = conn.execute(f"SELECT * FROM read_parquet('{fato_devolucoes}')").df()
    
    return df_vendas, df_dev

df_vendas, df_dev = load_base_data()
df_vendas['placed_at'] = pd.to_datetime(df_vendas['placed_at'])

# ==========================================
# 3. FILTROS (SIDEBAR)
# ==========================================
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3211/3211158.png", width=50) 
st.sidebar.title("Filtros Analíticos")

# Filtro de Período
anos_disponiveis = sorted(df_vendas['placed_at'].dt.year.unique())
anos_selecionados = st.sidebar.multiselect("Período (Ano):", options=anos_disponiveis, default=anos_disponiveis)

# Filtro de Canal
canais_disponiveis = df_vendas['channel'].unique()
# Tradução visual dos canais
canal_map = {'ecommerce': 'E-commerce', 'store': 'Lojas Físicas'}
df_vendas['Canal_Formatado'] = df_vendas['channel'].map(canal_map).fillna(df_vendas['channel'])
canais_formatados = df_vendas['Canal_Formatado'].unique()

canais_selecionados = st.sidebar.multiselect("Canal de Venda:", options=canais_formatados, default=canais_formatados)

if not anos_selecionados: anos_selecionados = anos_disponiveis
if not canais_selecionados: canais_selecionados = canais_formatados

# Aplicação
df_vendas_filt = df_vendas[
    (df_vendas['placed_at'].dt.year.isin(anos_selecionados)) & 
    (df_vendas['Canal_Formatado'].isin(canais_selecionados))
]

# ==========================================
# 4. STORYTELLING - CAMADA 1: CONTEXTO
# ==========================================
st.title("Desempenho Comercial e Operacional")
st.markdown(f"**Visão Executiva LH Nautical** | Analisando faturamento, comportamento de clientes e gargalos logísticos no período selecionado.")
st.markdown("---")

if df_vendas_filt.empty:
    st.warning("Não há dados para os filtros selecionados.")
    st.stop()

# ==========================================
# 5. STORYTELLING - CAMADA 2: KPIs (VISÃO EXECUTIVA)
# ==========================================
receita_total = df_vendas_filt['item_revenue'].sum()
margem_total = df_vendas_filt['gross_margin'].sum()
ticket_medio = receita_total / df_vendas_filt['order_id'].nunique()
clientes_ativos = df_vendas_filt['customer_id'].nunique()
margem_perc = (margem_total / receita_total) * 100 if receita_total > 0 else 0

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Receita Bruta", f"R$ {receita_total/1e6:,.1f} Mi".replace(",", "X").replace(".", ",").replace("X", "."))
col2.metric("Margem Bruta (R$)", f"R$ {margem_total/1e6:,.1f} Mi".replace(",", "X").replace(".", ",").replace("X", "."))
col3.metric("Margem (%)", f"{margem_perc:.1f}%".replace(".", ","))
col4.metric("Ticket Médio", f"R$ {ticket_medio:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."))
col5.metric("Clientes Ativos", f"{clientes_ativos:,}".replace(",", "."))

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 6. STORYTELLING - CAMADA 3: EVOLUÇÃO
# ==========================================
st.subheader("Receita apresenta fortes picos concentrados no período de Verão")
st.markdown("Acompanhamento mensal do faturamento reflete a alta dependência climática e sazonal dos produtos náuticos.")

df_ts = df_vendas_filt.groupby(pd.Grouper(key='placed_at', freq='ME'))['item_revenue'].sum().reset_index()
fig_ts = px.area(df_ts, x='placed_at', y='item_revenue', 
                 color_discrete_sequence=['#0284c7'])
fig_ts.update_layout(xaxis_title="", yaxis_title="Receita (R$)", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0))
fig_ts.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#e2e8f0')
st.plotly_chart(fig_ts, use_container_width=True)


# ==========================================
# 7. STORYTELLING - CAMADA 4: DIAGNÓSTICO (PRODUTOS E CLIENTES)
# ==========================================
st.markdown("---")
col_diag1, col_diag2 = st.columns(2)

with col_diag1:
    st.subheader("Categorias de alto ticket lideram faturamento")
    df_cat = df_vendas_filt.groupby('category_name')['item_revenue'].sum().reset_index().sort_values('item_revenue', ascending=False).head(5)
    fig_cat = px.bar(df_cat, y='category_name', x='item_revenue', orientation='h', 
                     color_discrete_sequence=['#10b981'])
    fig_cat.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Receita (R$)", yaxis_title="", plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_cat, use_container_width=True)

with col_diag2:
    st.subheader("Concentração B2C: 70%+ dos clientes formam o caixa")
    
    df_pareto = df_vendas_filt.groupby('customer_id')['item_revenue'].sum().reset_index()
    df_pareto = df_pareto.sort_values('item_revenue', ascending=False).reset_index(drop=True)
    df_pareto['receita_acumulada'] = df_pareto['item_revenue'].cumsum()
    df_pareto['perc_receita'] = (df_pareto['receita_acumulada'] / df_pareto['item_revenue'].sum()) * 100
    df_pareto['perc_clientes'] = (np.arange(1, len(df_pareto) + 1) / len(df_pareto)) * 100
    
    ponto_80_idx = df_pareto[df_pareto['perc_receita'] >= 80].index[0] if not df_pareto.empty else 0
    perc_clientes_80 = df_pareto.loc[ponto_80_idx, 'perc_clientes'] if not df_pareto.empty else 0
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(x=df_pareto['perc_clientes'], y=df_pareto['perc_receita'], 
                                    mode='lines', line=dict(color='#f59e0b', width=3)))
    fig_pareto.add_shape(type="line", x0=0, y0=80, x1=perc_clientes_80, y1=80, line=dict(color="red", width=1, dash="dash"))
    fig_pareto.add_shape(type="line", x0=perc_clientes_80, y0=0, x1=perc_clientes_80, y1=80, line=dict(color="red", width=1, dash="dash"))
    
    fig_pareto.update_layout(xaxis_title="% de Clientes", yaxis_title="% de Receita", plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_pareto, use_container_width=True)


# ==========================================
# 8. STORYTELLING - CAMADA 5: OFENSORES E AÇÕES
# ==========================================
st.markdown("---")
st.subheader("O Ralo Logístico: Desistências e Avarias geram o maior volume de estornos")
st.markdown("Análise dos motivos de devolução reportados no SAC. Foco em melhorar Tabela de Medidas (UX) e Auditoria de Transporte.")

# Ajustar devoluções ao filtro de ano aproximado
if 'return_date' in df_dev.columns:
    df_dev['return_date'] = pd.to_datetime(df_dev['return_date'])
    df_dev_filt = df_dev[df_dev['return_date'].dt.year.isin(anos_selecionados)]
else:
    df_dev_filt = df_dev

df_motivos = df_dev_filt.groupby('return_reason')['item_refund_total'].sum().reset_index().sort_values('item_refund_total', ascending=True)

fig_dev = px.bar(df_motivos, x='item_refund_total', y='return_reason', orientation='h', 
                 color_discrete_sequence=['#ef4444'])
fig_dev.update_layout(xaxis_title="Volume Financeiro Estornado (R$)", yaxis_title="Motivo do SAC", plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=10, b=0), height=300)
st.plotly_chart(fig_dev, use_container_width=True)

# ==========================================
# 9. FERRAMENTA DE AÇÃO: MOTOR DE RECOMENDAÇÃO
# ==========================================
with st.expander("🛠️ Ferramenta Acionável: Simulador de Cross-Sell (IA de Recomendação)"):
    st.markdown("Cruze histórico de carrinhos em tempo real para descobrir quais produtos oferecer em campanhas de CRM e no Checkout.")
    
    top_prods = df_vendas_filt.groupby(['product_name', 'sku']).size().reset_index(name='freq').sort_values('freq', ascending=False).head(50)
    
    if not top_prods.empty:
        col_rec1, col_rec2 = st.columns([1, 2])
        with col_rec1:
            selected_prod = st.selectbox("Selecione o Produto âncora:", top_prods['product_name'])
            selected_sku = top_prods[top_prods['product_name'] == selected_prod]['sku'].iloc[0]
            btn_gerar = st.button("Buscar Afinidades", type="primary", use_container_width=True)
            
        with col_rec2:
            if btn_gerar:
                with st.spinner("Analisando matriz..."):
                    fato_vendas_path = "E:/repo/lh_nautical_analise/data/processed/fato_vendas.parquet"
                    query_afinidade = f"""
                    WITH itens_carrinho AS (
                        SELECT order_id, sku, product_name FROM read_parquet('{fato_vendas_path}')
                    ),
                    pares AS (
                        SELECT b.product_name AS nome_recomendado, COUNT(*) as vezes_comprados_juntos
                        FROM itens_carrinho a
                        JOIN itens_carrinho b ON a.order_id = b.order_id AND a.sku != b.sku
                        WHERE a.sku = '{selected_sku}'
                        GROUP BY 1
                    )
                    SELECT nome_recomendado as "Produto Recomendado", vezes_comprados_juntos as "Vezes no mesmo carrinho"
                    FROM pares
                    WHERE vezes_comprados_juntos > 1
                    ORDER BY vezes_comprados_juntos DESC LIMIT 3
                    """
                    recs = con.execute(query_afinidade).df()
                    
                    if recs.empty:
                        st.info("Sem correlação estatística suficiente. Acionar 'Mais Vendidos da Categoria'.")
                    else:
                        st.dataframe(recs, use_container_width=True, hide_index=True)
