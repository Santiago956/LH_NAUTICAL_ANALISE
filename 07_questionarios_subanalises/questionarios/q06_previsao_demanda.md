# Questão 6 - Previsão de demanda

## Cenário

O Sr. Almir está furioso. No último verão, o estoque de "Coletes Salva-Vidas" acabou em 3 meses, e a empresa perdeu milhares de reais em vendas. Por outro lado, compraram "Âncoras" demais e elas estão enferrujando no galpão. Gabriel Santos, o Tech Lead, disse que não dá mais para confiar no "feeling". Ele quer um modelo preditivo que diga exatamente quantas unidades venderemos no próximo mês para ajustar as compras com fornecedores.

## Premissas obrigatórias

- O período de treino deve incluir dados até 31/12/2025.
- O período de teste deve ser o primeiro trimestre de 2026.
- A previsão deve ser feita em base mensal.
- Considere apenas o produto: "Bússola de Bordo 702".

## Tarefa

1. Utilize os datasets products.csv, product_variants, orders.csv e order_items.csv para criar um dataset unificado que facilite a criação do modelo preditivo.
2. Construa um modelo baseline simples, utilizando: Média móvel dos últimos 3 meses de vendas (considerando apenas dados anteriores à data prevista).
3. Gere a previsão mensal de vendas para o primeiro trimestre de 2026.
4. Compare as previsões com os valores reais do período de teste utilizando a métrica: MAE (Mean Absolute Error).
5. Responda objetivamente:
     a. O baseline é adequado para esse produto?
     b. Cite uma limitação desse método.
