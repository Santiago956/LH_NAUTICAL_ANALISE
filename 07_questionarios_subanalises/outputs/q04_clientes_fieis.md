# Questao 4 - Analise de clientes fieis

## Codigo SQL

O SQL da entrega esta em:

```text
07_questionarios_subanalises/outputs/q04_clientes_fieis.sql
```

## Resultado validado nos CSVs

### Top 10 clientes fieis

| customer_id | faturamento_total | frequencia | ticket_medio | diversidade_categorias |
| ---: | ---: | ---: | ---: | ---: |
| 22 | 1.087.838,44 | 26 | 41.839,94 | 14 |
| 1477 | 916.262,58 | 22 | 41.648,30 | 14 |
| 929 | 1.082.775,89 | 26 | 41.645,23 | 14 |
| 1116 | 655.737,20 | 16 | 40.983,58 | 14 |
| 1691 | 815.471,30 | 20 | 40.773,57 | 14 |
| 774 | 726.127,99 | 18 | 40.340,44 | 14 |
| 1470 | 1.040.553,09 | 26 | 40.021,27 | 14 |
| 1599 | 997.616,46 | 25 | 39.904,66 | 14 |
| 965 | 677.297,78 | 17 | 39.841,05 | 14 |
| 1722 | 1.146.455,22 | 29 | 39.532,94 | 14 |

### Categoria com maior quantidade comprada pelo grupo

| category_id | categoria | quantidade_total_itens |
| ---: | --- | ---: |
| 8 | Helices | 492 |

## Diagnostico

**Fato observado:** Os 10 clientes fieis possuem ticket medio entre aproximadamente 39,5 mil e 41,8 mil por transacao e compraram em 14 categorias distintas.

**Hipotese:** Esse grupo combina alto valor por pedido com comportamento amplo de compra, indicando clientes que usam a LH Nautical como fornecedor recorrente para diferentes necessidades nauticas, nao apenas para uma compra pontual de alto valor.

**Recomendacao:** Usar a categoria `Helices` como ponto de partida para campanhas de cross-sell e analise de cesta desses clientes, pois foi a categoria com maior volume de itens comprados dentro do grupo de elite.
