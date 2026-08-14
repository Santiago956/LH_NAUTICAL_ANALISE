import pandas as pd
import numpy as np
import duckdb

def main():
    conn = duckdb.connect()
    
    query = """
    SELECT 
        o.customer_id,
        p.id AS product_id,
        p.name AS product_name
    FROM read_csv_auto('data/raw/orders.csv') o
    JOIN read_csv_auto('data/raw/order_items.csv') oi ON o.id = oi.order_id
    JOIN read_csv_auto('data/raw/product_variants.csv') pv ON oi.product_variant_id = pv.id
    JOIN read_csv_auto('data/raw/products.csv') p ON pv.product_id = p.id
    WHERE o.status != 'cancelled'
    GROUP BY 1, 2, 3
    """
    
    df = conn.execute(query).df()
    conn.close()
    
    # Adiciona a coluna de interação (presença = 1)
    df['interaction'] = 1
    
    # Cria a matriz Usuário x Produto
    # Linhas: customer_id, Colunas: product_name (usamos name para facilitar a visualização)
    matrix = pd.pivot_table(df, index='customer_id', columns='product_name', values='interaction', aggfunc='max', fill_value=0)
    
    # Produto de referência
    target_product = "Motor de Popa 1949"
    
    if target_product not in matrix.columns:
        print(f"Erro: Produto {target_product} não encontrado na matriz.")
        return
        
    # Vetor do produto alvo
    target_vector = matrix[target_product].values
    target_norm = np.linalg.norm(target_vector)
    
    similarities = {}
    
    for product in matrix.columns:
        if product == target_product:
            continue
            
        vector = matrix[product].values
        norm = np.linalg.norm(vector)
        
        if norm == 0 or target_norm == 0:
            sim = 0
        else:
            sim = np.dot(target_vector, vector) / (target_norm * norm)
            
        similarities[product] = sim
        
    # Ranking
    ranking = pd.Series(similarities).sort_values(ascending=False).head(5)
    
    print(f"Top 5 recomendações para quem comprou '{target_product}':")
    for i, (prod, sim) in enumerate(ranking.items(), 1):
        print(f"{i}. {prod} (Similaridade: {sim:.4f})")

if __name__ == '__main__':
    main()
