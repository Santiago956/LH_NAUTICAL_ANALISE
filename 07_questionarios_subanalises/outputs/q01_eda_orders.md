# Questao 1 - EDA: tabela `orders`

## SQL

```sql
SELECT
    COUNT(*) AS total_linhas,
    MIN(created_at) AS data_minima_created_at,
    MAX(created_at) AS data_maxima_created_at,
    MIN(total) AS valor_minimo_total,
    MAX(total) AS valor_maximo_total,
    AVG(total) AS valor_medio_total,
    SUM(CASE WHEN created_at IS NULL THEN 1 ELSE 0 END) AS created_at_nulos,
    SUM(CASE WHEN total IS NULL THEN 1 ELSE 0 END) AS total_nulos,
    SUM(CASE WHEN total < 0 THEN 1 ELSE 0 END) AS total_negativo,
    SUM(CASE WHEN total = 0 THEN 1 ELSE 0 END) AS total_zero
FROM orders;
```

## Resultado observado

| Metrica | Valor |
| --- | ---: |
| Quantidade total de linhas | 48.998 |
| Menor `created_at` | 2020-01-01 01:19:28 |
| Maior `created_at` | 2026-12-31 23:43:09 |
| Menor `total` | 32,62 |
| Maior `total` | 127.262,02 |
| Media de `total` | 28.704,99 |
| `created_at` nulos | 0 |
| `total` nulos | 0 |
| `total` negativo | 0 |
| `total` igual a zero | 0 |

## Diagnostico resumido

**Fato observado:** A tabela `orders` possui 48.998 pedidos, cobrindo registros de 2020-01-01 a 2026-12-31. A coluna `total` nao possui valores nulos, negativos ou zerados nesta verificacao inicial.

**Hipotese:** O valor maximo de `total` e alto em relacao ao minimo e a media, o que pode indicar pedidos corporativos, compras de itens nauticos de alto valor ou possiveis outliers comerciais. Como nao houve limpeza nem cruzamento com itens do pedido, ainda nao e possivel afirmar se o valor extremo e erro.

**Recomendacao:** A tabela parece estruturalmente confiavel para uma EDA inicial, pois nao apresenta problemas basicos em `created_at` e `total`. Para analises decisorias, ela ainda exige tratamento previo: validar o corte temporal, investigar extremos de `total`, conferir status dos pedidos e cruzar com itens, pagamentos e devolucoes antes de concluir receita, lucro ou performance.
