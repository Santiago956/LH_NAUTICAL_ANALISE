import streamlit as st
import duckdb
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# --- CONFIGURAÇÃO DA PÁGINA E CSS PREMIUM ---
st.set_page_config(page_title="LH Nautical | Executive Analytics", page_icon="⛵", layout="wide", initial_sidebar_state="expanded")

# CSS para tornar o design muito mais moderno (Glassmorphism e tipografia premium)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    html, body, [class*="css"]  {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Estilização dos Cards de KPI */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: 600 !important;
        color: #0ea5e9 !important; /* Azul moderno */
    }
    div[data-testid="stMetricLabel"] {
        font-size: 16px !important;
        font-weight: 400 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Background dos Cards para parecer "Premium" */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0));
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.18);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        border-radius: 10px;
        padding: 15px;
    }
    
    /* Ajustando os títulos das abas */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 600;
    }
    
    h1, h2, h3 {
        font-family: 'Outfit', sans-serif !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- CARREGAMENTO DE DADOS (CACHE) ---
@st.cache_resource
def get_db_connection():
    return duckdb.connect()

con = get_db_connection()

@st.cache_data
def load_base_data():
    conn = duckdb.connect()
    fato_vendas = "E:/repo/lh_nautical_analise/data/processed/fato_vendas.parquet"
    fato_devolucoes = "E:/repo/lh_nautical_analise/data/processed/fato_devolucoes.parquet"
    dim_clientes = "E:/repo/lh_nautical_analise/data/processed/dim_clientes.parquet"
    categories = "E:/repo/lh_nautical_analise/data/raw/categories.csv"
    
    # Base inteira de vendas em memória (Pandas)
    df_vendas = conn.execute(f"""
        SELECT 
            f.order_id, f.placed_at, f.channel, f.item_revenue, f.gross_margin, 
            f.customer_id, f.sku, f.product_name, c.name as category_name
        FROM read_parquet('{fato_vendas}') f
        LEFT JOIN read_csv_auto('{categories}') c ON f.category_id = c.id
    """).df()
    
    # Base de devoluções
    df_dev = conn.execute(f"SELECT * FROM read_parquet('{fato_devolucoes}')").df()
    
    # Clientes
    df_clientes = conn.execute(f"SELECT * FROM read_parquet('{dim_clientes}')").df()
    
    return df_vendas, df_dev, df_clientes

df_vendas, df_dev, df_clientes = load_base_data()
df_vendas['placed_at'] = pd.to_datetime(df_vendas['placed_at'])

# --- SIDEBAR: SEGMENTAÇÃO ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/3211/3211158.png", width=60) # Anchor icon
st.sidebar.title("Filtros Executivos")

# Filtro de Ano
anos = sorted(df_vendas['placed_at'].dt.year.unique())
anos_selecionados = st.sidebar.multiselect("Selecione o(s) Ano(s):", options=anos, default=anos)

# Filtro de Canal
canais = df_vendas['channel'].unique()
canais_selecionados = st.sidebar.multiselect("Canal de Venda:", options=canais, default=canais)

# Aplicação dos Filtros nas Bases
if not anos_selecionados: anos_selecionados = anos
if not canais_selecionados: canais_selecionados = canais

df_vendas_filtered = df_vendas[
    (df_vendas['placed_at'].dt.year.isin(anos_selecionados)) & 
    (df_vendas['channel'].isin(canais_selecionados))
]

# --- CABEÇALHO ---
st.title("⛵ LH Nautical Analytics")
st.markdown("Dashboard executivo interativo focado em lucratividade e comportamento de clientes.")
st.markdown("---")

# --- ABAS ---
tab1, tab2, tab3, tab4 = st.tabs(["📊 Visão Geral", "🎯 Clientes & Pareto", "📦 Operações (Devoluções)", "🤖 Motor de IA"])

# === ABA 1: VISÃO GERAL ===
with tab1:
    st.subheader("Indicadores Chave de Performance (KPIs)")
    # KPIs dinâmicos baseados no filtro
    receita_total = df_vendas_filtered['item_revenue'].sum()
    margem_total = df_vendas_filtered['gross_margin'].sum()
    ticket_medio = receita_total / df_vendas_filtered['order_id'].nunique() if not df_vendas_filtered.empty else 0
    total_pedidos = df_vendas_filtered['order_id'].nunique()
    clientes_ativos = df_vendas_filtered['customer_id'].nunique()
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💰 Receita Total", f"R$ {receita_total/1e6:,.2f} Mi".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("📈 Margem Bruta", f"R$ {margem_total/1e6:,.2f} Mi".replace(",", "X").replace(".", ",").replace("X", "."))
    col3.metric("🛒 Ticket Médio", f"R$ {ticket_medio:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col4.metric("👥 Clientes Ativos", f"{clientes_ativos:,}".replace(",", "."))
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Gráficos da Visão Geral
    col_chart1, col_chart2 = st.columns([6, 4])
    
    with col_chart1:
        # Sazonalidade Dinâmica
        df_ts = df_vendas_filtered.groupby(pd.Grouper(key='placed_at', freq='ME'))['item_revenue'].sum().reset_index()
        fig_ts = px.area(df_ts, x='placed_at', y='item_revenue', title="Evolução da Receita (Sazonalidade de Verão)",
                         template="plotly_dark", color_discrete_sequence=['#38bdf8'])
        fig_ts.update_layout(xaxis_title="", yaxis_title="Receita (R$)", font=dict(family="Outfit", size=14))
        st.plotly_chart(fig_ts, use_container_width=True)
        
    with col_chart2:
        # Categorias Dinâmico
        df_cat = df_vendas_filtered.groupby('category_name')['item_revenue'].sum().reset_index().sort_values('item_revenue', ascending=False).head(8)
        fig_cat = px.bar(df_cat, y='category_name', x='item_revenue', orientation='h', title="Top 8 Categorias",
                         template="plotly_dark", color_discrete_sequence=['#10b981'])
        fig_cat.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="", yaxis_title="", font=dict(family="Outfit", size=14))
        st.plotly_chart(fig_cat, use_container_width=True)


# === ABA 2: CLIENTES (PARETO DINÂMICO) ===
with tab2:
    st.subheader("Curva de Concentração (Pareto)")
    
    # Cálculo do Pareto em tempo real
    df_pareto = df_vendas_filtered.groupby('customer_id')['item_revenue'].sum().reset_index()
    df_pareto = df_pareto.sort_values('item_revenue', ascending=False).reset_index(drop=True)
    df_pareto['receita_acumulada'] = df_pareto['item_revenue'].cumsum()
    df_pareto['perc_receita'] = (df_pareto['receita_acumulada'] / df_pareto['item_revenue'].sum()) * 100
    df_pareto['perc_clientes'] = (np.arange(1, len(df_pareto) + 1) / len(df_pareto)) * 100
    
    # Encontrar o ponto onde bate 80% da receita
    try:
        ponto_80_idx = df_pareto[df_pareto['perc_receita'] >= 80].index[0]
        perc_clientes_80 = df_pareto.loc[ponto_80_idx, 'perc_clientes']
    except IndexError:
        perc_clientes_80 = 0
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Scatter(x=df_pareto['perc_clientes'], y=df_pareto['perc_receita'], 
                                    mode='lines', name='Curva de Concentração', line=dict(color='#f59e0b', width=4)))
    
    # Linhas de marcação dos 80%
    fig_pareto.add_shape(type="line", x0=0, y0=80, x1=perc_clientes_80, y1=80, line=dict(color="red", width=2, dash="dash"))
    fig_pareto.add_shape(type="line", x0=perc_clientes_80, y0=0, x1=perc_clientes_80, y1=80, line=dict(color="red", width=2, dash="dash"))
    fig_pareto.add_annotation(x=perc_clientes_80, y=80, text=f"{perc_clientes_80:.1f}% dos clientes", showarrow=True, arrowhead=1, ax=50, ay=30)
    
    fig_pareto.update_layout(title="Distribuição de Receita por Cliente (Quebra do Mito 80/20)", 
                             xaxis_title="% de Clientes Acumulados", yaxis_title="% de Receita Acumulada",
                             template="plotly_dark", font=dict(family="Outfit", size=14), height=500)
    
    st.plotly_chart(fig_pareto, use_container_width=True)
    
    st.info(f"💡 **Insight Estratégico:** Nos filtros selecionados, precisamos de **{perc_clientes_80:.1f}%** dos clientes para compor 80% da receita. Isso confirma a característica B2C Varejista da LH Nautical.")


# === ABA 3: OPERAÇÕES (DEVOLUÇÕES) ===
with tab3:
    st.subheader("Análise de Fricção (Devoluções)")
    
    # Filtrando devoluções de forma aproximada baseado nos filtros de tempo (para simplificar, aplicamos na data da devolução)
    if 'return_date' in df_dev.columns:
        df_dev['return_date'] = pd.to_datetime(df_dev['return_date'])
        df_dev_filt = df_dev[df_dev['return_date'].dt.year.isin(anos_selecionados)]
    else:
        df_dev_filt = df_dev # fallback se o formato da data variar
        
    df_motivos = df_dev_filt.groupby('return_reason')['item_refund_total'].sum().reset_index().sort_values('item_refund_total', ascending=False)
    
    fig_dev = px.bar(df_motivos, x='item_refund_total', y='return_reason', orientation='h', 
                     title="Impacto Financeiro por Motivo (Estornos)", 
                     color='item_refund_total', color_continuous_scale='Reds', template="plotly_dark")
    fig_dev.update_layout(yaxis={'categoryorder':'total ascending'}, xaxis_title="Valor Estornado (R$)", yaxis_title="", font=dict(family="Outfit", size=14))
    
    col1, col2 = st.columns([7, 3])
    with col1:
        st.plotly_chart(fig_dev, use_container_width=True)
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.warning("⚠️ **Alerta Logístico:**\n\nProblemas com transporte (Avarias) e problemas de UX na plataforma (Desistências/Tamanho Errado) representam a esmagadora maioria do 'ralo' financeiro da companhia.")


# === ABA 4: SIMULADOR DE IA ===
with tab4:
    st.subheader("🤖 Motor de Recomendação (Cross-Sell)")
    st.markdown("Nosso algoritmo identifica produtos frequentemente comprados no mesmo carrinho. Selecione um item abaixo para simular a vitrine.")
    
    # Para performance, pré-calculamos os top produtos da base filtrada
    top_prods = df_vendas_filtered.groupby(['product_name', 'sku']).size().reset_index(name='freq').sort_values('freq', ascending=False).head(100)
    
    if not top_prods.empty:
        selected_prod = st.selectbox("Escolha um Produto (Vitrine):", top_prods['product_name'])
        selected_sku = top_prods[top_prods['product_name'] == selected_prod]['sku'].iloc[0]
        
        if st.button("Gerar Vitrine: Quem comprou isso, também levou...", type="primary"):
            with st.spinner("Varrendo centenas de milhares de carrinhos..."):
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
                SELECT nome_recomendado, vezes_comprados_juntos
                FROM pares
                WHERE vezes_comprados_juntos > 1
                ORDER BY vezes_comprados_juntos DESC LIMIT 3
                """
                recs = con.execute(query_afinidade).df()
                
                if recs.empty:
                    st.warning("Histórico insuficiente. Acionar vitrine de fallback ('Mais Vendidos').")
                else:
                    for i, row in recs.iterrows():
                        st.info(f"🛒 **{row['nome_recomendado']}** (juntos {row['vezes_comprados_juntos']} vezes)")
