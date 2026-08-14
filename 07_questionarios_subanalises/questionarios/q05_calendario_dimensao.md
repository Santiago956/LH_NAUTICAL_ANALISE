# Questao 5 - Dimensao de calendario

## Cenario

O Sr. Almir quer saber: "Qual e o dia da semana (Segunda, Terca...), nas lojas fisicas, temos a pior media de vendas?" para decidir se vale a pena fechar a loja nesses dias.

Um estagiario fez um `GROUP BY dia_semana` direto na tabela de vendas e disse que o Domingo era otimo, com media de R$ 5.000,00.

O problema: o estagiario esqueceu que em muitos Domingos a loja abriu mas vendeu zero. Como esses dias nao existem na tabela de vendas (`orders`), eles foram ignorados no calculo da media, inflando o resultado. Precisamos corrigir isso utilizando um calendario de datas (dimensao de datas).

## Premissas obrigatorias

- O periodo de analise deve considerar todas as datas entre a menor e a data atual da venda presentes no arquivo.
- A loja esteve aberta em todos os dias do periodo (inclusive fins de semana).
- Considere apenas as lojas fisicas (`channel = pos`).
- Dias sem registro na tabela de vendas devem ser considerados como valor da venda = 0.
- "Vendas diarias" correspondem a soma de valor da venda por dia.
- A media de vendas por dia da semana deve considerar todos os dias do calendario, inclusive os dias sem venda.
- O nome do dia da semana deve ser apresentado em portugues (Segunda-feira, Terca-feira, etc.).

## Tarefa

- Construir uma dimensao de datas utilizando SQL.
- Cruzar a dimensao de datas com a tabela de vendas para analise.

## Entregas

Codigo com:

1. Desenvolvimento de um calendario com os dias da semana (em portugues).
2. `LEFT JOIN` entre o calendario e a tabela de vendas.
3. Agregacao de vendas por dia (soma de `valor_venda`).
4. Substituicao de valores nulos por zero para dias sem vendas.