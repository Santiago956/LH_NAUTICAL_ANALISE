"""
Questao 5 - Dimensao de calendario (validacao local com DuckDB)

Reproduz o resultado esperado do SQL PostgreSQL (outputs/q05_calendario_dimensao.sql)
sem exigir um banco PostgreSQL, usando os CSVs originais de data/raw.

A logica e identica ao SQL da entrega:
1. gera um calendario do menor ao maior created_at de orders;
2. agrega vendas diarias apenas do canal 'pos';
3. faz LEFT JOIN do calendario com as vendas e COALESCE(..., 0);
4. calcula a media por dia da semana considerando todos os dias.

Uso:
    uv run python 07_questionarios_subanalises/scripts/q05_validar_calendario_duckdb.py
"""

from pathlib import Path

import duckdb

RAIZ_PROJETO = Path(__file__).resolve().parents[2]
ARQUIVO_ORDERS = RAIZ_PROJETO / "data" / "raw" / "orders.csv"


def nome_dia_semana(dow):
    """Traduz EXTRACT(DOW) (0=Domingo ... 6=Sabado) para portugues."""
    nomes = [
        "Domingo",
        "Segunda-feira",
        "Terca-feira",
        "Quarta-feira",
        "Quinta-feira",
        "Sexta-feira",
        "Sabado",
    ]
    return nomes[dow]


def main():
    conexao = duckdb.connect()

    sql = """
    WITH RECURSIVE calendario AS (
        SELECT (SELECT MIN(created_at)::date FROM read_csv_auto(?) ) AS data
        UNION ALL
        SELECT data + INTERVAL '1 day'
        FROM calendario
        WHERE data < (SELECT MAX(created_at)::date FROM read_csv_auto(?))
    ),
    vendas_por_dia AS (
        SELECT
            created_at::date AS data,
            SUM(total)       AS valor_venda
        FROM read_csv_auto(?)
        WHERE channel = 'pos'
        GROUP BY created_at::date
    ),
    vendas_diarias AS (
        SELECT
            c.data,
            CASE EXTRACT(DOW FROM c.data)
                WHEN 0 THEN 'Domingo'
                WHEN 1 THEN 'Segunda-feira'
                WHEN 2 THEN 'Terca-feira'
                WHEN 3 THEN 'Quarta-feira'
                WHEN 4 THEN 'Quinta-feira'
                WHEN 5 THEN 'Sexta-feira'
                WHEN 6 THEN 'Sabado'
            END                AS dia_semana,
            COALESCE(v.valor_venda, 0) AS valor_venda
        FROM calendario c
        LEFT JOIN vendas_por_dia v
            ON v.data = c.data
    )
    SELECT
        dia_semana,
        COUNT(*)                                       AS dias_no_periodo,
        SUM(CASE WHEN valor_venda = 0 THEN 1 ELSE 0 END) AS dias_sem_venda,
        ROUND(SUM(valor_venda), 2)                     AS vendas_totais,
        ROUND(AVG(valor_venda), 2)                     AS media_vendas_por_dia
    FROM vendas_diarias
    GROUP BY dia_semana
    ORDER BY media_vendas_por_dia ASC;
    """

    caminho = str(ARQUIVO_ORDERS)
    resultado = conexao.execute(sql, [caminho, caminho, caminho]).df()
    conexao.close()

    print(resultado.to_string(index=False))

    pior_dia = resultado.iloc[0]
    print("\n--- Resposta ---")
    print(
        f"Pior media de vendas em lojas fisicas: {pior_dia['dia_semana']} "
        f"com R$ {pior_dia['media_vendas_por_dia']:,.2f} por dia "
        f"({int(pior_dia['dias_sem_venda'])} dias sem venda no periodo)."
    )


if __name__ == "__main__":
    main()