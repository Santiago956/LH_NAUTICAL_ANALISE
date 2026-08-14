import pandas as pd
import duckdb

def mean_absolute_error(y_true, y_pred):
    return sum(abs(a - b) for a, b in zip(y_true, y_pred)) / len(y_true)

def main():
    # 1. Unificar os datasets
    conn = duckdb.connect()
    
    query = """
    SELECT 
        DATE_TRUNC('month', o.created_at::DATE) AS month,
        SUM(oi.quantity) AS total_quantity
    FROM read_csv_auto('data/raw/orders.csv') o
    JOIN read_csv_auto('data/raw/order_items.csv') oi ON o.id = oi.order_id
    JOIN read_csv_auto('data/raw/product_variants.csv') pv ON oi.product_variant_id = pv.id
    JOIN read_csv_auto('data/raw/products.csv') p ON pv.product_id = p.id
    WHERE p.name = 'Bússola de Bordo 702'
      AND o.status != 'cancelled'
    GROUP BY 1
    ORDER BY 1
    """
    
    df = conn.execute(query).df()
    conn.close()
    
    # Ensure all months are present
    df['month'] = pd.to_datetime(df['month'])
    full_range = pd.date_range(start=df['month'].min(), end='2026-03-01', freq='MS')
    df = df.set_index('month').reindex(full_range, fill_value=0).reset_index()
    df.columns = ['month', 'total_quantity']
    
    print(df.tail(10))
    
    # 2. Construa o modelo baseline
    # Previsão iterativa (multi-step ahead)
    
    # Train data
    df_train = df[df['month'] <= '2025-12-01'].copy()
    
    # Previsões
    pred_jan = df_train['total_quantity'].iloc[-3:].mean()
    df_train.loc[len(df_train)] = [pd.to_datetime('2026-01-01'), pred_jan]
    
    pred_feb = df_train['total_quantity'].iloc[-3:].mean()
    df_train.loc[len(df_train)] = [pd.to_datetime('2026-02-01'), pred_feb]
    
    pred_mar = df_train['total_quantity'].iloc[-3:].mean()
    
    print(f"Previsões Q1 2026: Jan={pred_jan:.2f}, Feb={pred_feb:.2f}, Mar={pred_mar:.2f}")
    
    # Comparação
    df_test = df[(df['month'] >= '2026-01-01') & (df['month'] <= '2026-03-01')].copy()
    y_true = df_test['total_quantity'].values
    y_pred = [pred_jan, pred_feb, pred_mar]
    
    print("Valores Reais Q1 2026:", y_true)
    
    mae = mean_absolute_error(y_true, y_pred)
    print(f"MAE: {mae:.2f}")

if __name__ == '__main__':
    main()
