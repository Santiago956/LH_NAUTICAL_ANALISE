import streamlit as st
import duckdb
import pandas as pd
import plotly.express as px

# Configuração da Página
st.set_page_config(page_title="LH Nautical Dashboard", page_icon="⛵", layout="wide")

# Inicialização e Cache de Dados
@st.cache_data
def load_data():
    con = duckdb.connect()
    fato_vendas = "E:/repo/lh_nautical_analise/data/processed/fato_vendas.parquet"
    fato_devolucoes = "E:/repo/lh_nautical_analise/data/processed/fato_devolucoes.parquet"
    dim_clientes = "E:/repo/lh_nautical_analise/data/processed/dim_clientes.parquet"
    categories = "E:/repo/lh_nautical_analise/data/raw/categories.csv"
    
    # KPIs Básicos
    kpis = con.execute(f"SELECT SUM(item_revenue) as receita, SUM(gross_margin) as margem FROM read_parquet('{fato_vendas}')").df()
    
    # Sazonalidade
    df_ts = con.execute(f"""
        SELECT DATE_TRUNC('month', placed_at) as mes, SUM(item_revenue) as receita
        FROM read_parquet('{fato_vendas}')
        GROUP BY 1 ORDER BY 1
    """).df()
    
    # Categorias
    df_cat = con.execute(f"""
        SELECT c.name as categoria, SUM(f.item_revenue) as receita
        FROM read_parquet('{fato_vendas}') f
        LEFT JOIN read_csv_auto('{categories}') c ON f.category_id = c.id
        GROUP BY 1 ORDER BY 2 DESC LIMIT 10
    """).df()
    
    # Devoluções
    df_dev = con.execute(f"""
        SELECT return_reason as motivo, SUM(item_refund_total) as valor_estornado
        FROM read_parquet('{fato_devolucoes}')
        GROUP BY 1 ORDER BY 2 DESC
    """).df()
    
    return con, fato_vendas, kpis, df_ts, df_cat, df_dev

con, fato_vendas, kpis, df_ts, df_cat, df_dev = load_data()

# Título Principal
st.title("⛵ LH Nautical - Centro de Inteligência Executiva")
st.markdown("---")

# Abas do Dashboard
tab1, tab2, tab3, tab4 = st.tabs(["📈 Visão Geral", "👥 Clientes (Pareto)", "📦 Ralo Logístico", "🤖 IA & Cross-Sell"])

# --- ABA 1: VISÃO GERAL ---
with tab1:
    col1, col2 = st.columns(2)
    col1.metric("Receita Total (R$)", f"R$ {kpis['receita'].iloc[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("Margem Bruta (R$)", f"R$ {kpis['margem'].iloc[0]:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.subheader("Faturamento Mensal (Sazonalidade)")
    fig_ts = px.line(df_ts, x='mes', y='receita', title="Picos Fortes no Verão (Dez-Fev)", markers=True)
    st.plotly_chart(fig_ts, use_container_width=True)
    
    st.subheader("Top Categorias de Produtos")
    fig_cat = px.bar(df_cat, x='receita', y='categoria', orientation='h', title="As categorias 'Pesadas' lideram o faturamento")
    fig_cat.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_cat, use_container_width=True)


# --- ABA 2: CLIENTES ---
with tab2:
    st.subheader("Concentração de Receita B2C (Curva ABC)")
    st.markdown("**Insight:** Ao contrário do mito do 80/20, precisamos de **71.6% dos clientes** para formar 80% do faturamento. Nosso foco é massa, não VIPs.")
    st.image(r"E:\repo\lh_nautical_analise\docs\plot_pareto.png", use_container_width=True)


# --- ABA 3: DEVOLUÇÕES ---
with tab3:
    st.subheader("Impacto Financeiro por Motivo de Devolução")
    fig_dev = px.bar(df_dev, x='valor_estornado', y='motivo', orientation='h', title="Fricção Digital (Desistência/Tamanho) e Física (Avarias) dominam", color='valor_estornado', color_continuous_scale='Reds')
    fig_dev.update_layout(yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig_dev, use_container_width=True)
    st.info("Recomendação: Melhorar a tabela de medidas no site (UX) e realizar auditoria com as transportadoras sobre avarias.")


# --- ABA 4: RECOMENDAÇÃO ---
with tab4:
    st.subheader("🛍️ Motor de Recomendação (Simulador)")
    st.markdown("Selecione um produto para descobrir o que os clientes costumam comprar junto, baseado na nossa Matriz de Co-ocorrência em SQL.")
    
    # Pegar lista de produtos (limitado aos 100 mais vendidos para não pesar no select box)
    @st.cache_data
    def get_top_products():
        return con.execute(f"SELECT product_name, sku, COUNT(*) as freq FROM read_parquet('{fato_vendas}') GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 100").df()
    
    top_prods = get_top_products()
    selected_prod = st.selectbox("Escolha um Produto (Top 100 Mais Vendidos):", top_prods['product_name'])
    selected_sku = top_prods[top_prods['product_name'] == selected_prod]['sku'].iloc[0]
    
    if st.button("Gerar Recomendações"):
        with st.spinner("Analisando milhares de carrinhos..."):
            query_afinidade = f"""
            WITH itens_carrinho AS (
                SELECT order_id, sku, product_name FROM read_parquet('{fato_vendas}')
            ),
            pares AS (
                SELECT a.sku AS id_produto_ancora, b.sku AS id_produto_recomendado, b.product_name AS nome_recomendado
                FROM itens_carrinho a
                JOIN itens_carrinho b ON a.order_id = b.order_id AND a.sku != b.sku
                WHERE a.sku = '{selected_sku}'
            )
            SELECT id_produto_recomendado, nome_recomendado, COUNT(*) as vezes_comprados_juntos
            FROM pares
            GROUP BY 1, 2
            HAVING vezes_comprados_juntos > 1
            ORDER BY vezes_comprados_juntos DESC LIMIT 3
            """
            recs = con.execute(query_afinidade).df()
            
            if recs.empty:
                st.warning("Não há histórico de compras conjuntas suficiente para este item (Recomendar 'Mais Vendidos').")
            else:
                st.success(f"Clientes que compraram **{selected_prod}** também levaram:")
                for i, row in recs.iterrows():
                    st.write(f"- 🛒 **{row['nome_recomendado']}** (juntos {row['vezes_comprados_juntos']} vezes)")
