# Questao 4 - Analise de clientes

## Cenario

A Diretoria da LH Nautical deseja identificar clientes fieis. Diferente de quem compra muito uma unica vez, o cliente fiel e aquele que possui gasto medio alto por transacao e navega por diversas categorias da loja.

O objetivo e mapear o que esses clientes de elite estao consumindo para replicar o comportamento em outros segmentos.

## Premissas obrigatorias

- Faturamento Total: soma da coluna `total` por cliente.
- Frequencia: contagem total de transacoes, ou IDs de venda, por cliente.
- Ticket Medio: Faturamento Total / Frequencia.
- Diversidade de Categorias: quantidade de categorias distintas (`category_id`) que o cliente comprou.
- Filtro de Elite: apenas clientes que compraram produtos de 13 ou mais categorias distintas entram no ranking.
- Desempate: em caso de empate no Ticket Medio, usar `customer_id` em ordem crescente.

## Tarefa

- Calcular Ticket Medio e Diversidade de Categorias por `customer_id`.
- Filtrar os 10 clientes com maior Ticket Medio entre aqueles com diversidade maior ou igual a 13 categorias.
- Para esse grupo de 10 clientes, identificar a categoria com maior quantidade total de itens comprados (`SUM(quantity)`).
