# Questão 7 - Sistema de recomendação

## Cenário

A Marina percebeu que clientes que compram lanchas quase sempre esquecem de levar a defensa (proteção lateral). Ela quer implementar uma vitrine de "Quem comprou isso, também levou..." no site. 

Como não temos ferramentas de Big Data caras, você precisará criar um motor de recomendação, baseado na similaridade de compra dos clientes. 

Identificar qual produto deve ser recomendado junto ao item “Motor de Popa 1949”, com base na similaridade de comportamento de compra dos clientes.

## Tarefa

1. Crie uma matriz de interação Usuário × Produto obedecendo às regras abaixo:
     a. Linhas: id_cliente
     b. Colunas: id_produto
     c. Valor da célula:
     d. 1 se o cliente comprou ao menos uma vez o produto
     e. 0 caso contrário
     f. Ignore a quantidade comprada (presença/ ausência apenas)
2. Cálculo de Similaridade entre Produtos
     a. Calcule a Similaridade de Cosseno (Cosine Similarity) entre os vetores dos produtos
     b. A similaridade deve ser calculada produto × produto, com base nos clientes que compraram cada item
3. Ranking de Produtos Similares
     a. Considere o produto “Motor de Popa 1949” como item de referência
     b. Gere um ranking com os nomes dos 5 produtos mais similares a ele
     c. Desconsidere o próprio motor no ranking 
     d. Script em python que constrói a matriz, calcula similaridade e gera o ranking usando bibliotecas permitidas (pandas, numpy).
