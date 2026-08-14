# Questão 7 - Sistema de recomendação

## Tema do desafio
- Tema principal: Sistema de recomendação (item 6).
- Tema secundário: Tratamento de dados (item 2) - Pivot e transformação de base em vetores.
- Stakeholder principal: Marina Costa (Gerente de Negócios).

## Objetivo de negócio
Criar uma vitrine do tipo "Quem comprou isso, também levou...", sugerindo itens relevantes no momento da compra (cross-selling) para aumentar o ticket médio e prevenir esquecimentos (ex: defesa para lancha).

## Metodologia Aplicada
Como não há ferramentas pesadas de Big Data, o modelo utilizou a **Similaridade de Cosseno** (Cosine Similarity) baseada em Filtro Colaborativo Item a Item (Item-based Collaborative Filtering) com informações implícitas (comprou / não comprou).

1. **Matriz Usuário x Produto:** Foram criadas linhas para cada `customer_id` e colunas para cada `product_name`. Se o cliente comprou o produto (mesmo que mais de uma vez ou em quantidades variadas), a célula recebeu `1`, caso contrário `0`.
2. **Similaridade:** Para cada produto, o seu "vetor de clientes" foi comparado com os demais através do produto escalar dividido pela multiplicação das normas vetoriais (Cosseno).
3. **Produto Alvo:** "Motor de Popa 1949".

## Resultado

O script em Python processou as vendas não-canceladas e comparou a base de usuários do **Motor de Popa 1949** com o restante do catálogo. 

Abaixo estão os 5 produtos recomendados para a vitrine "Quem comprou isso, também levou", ranqueados pela força do relacionamento de compra conjunta (Similaridade de Cosseno):

| Ranking | Produto Recomendado | Score de Similaridade |
| :---: | :--- | :---: |
| 1º | Vela Mestra 1913 | 0.2588 |
| 2º | Cabo Náutico 2105 | 0.2460 |
| 3º | asdf | 0.2392 |
| 4º | Sonar Transducer 7193 | 0.2316 |
| 5º | Motor de Popa 5331 | 0.2263 |

> **Nota de qualidade de dados:** O produto "asdf" aparece no ranking na 3ª posição, indicando um dado de teste ou cadastro de produto sujo na base `products.csv` real que acabou sendo comprado simultaneamente com o motor. Limpezas e inativação de produtos testes (`is_active = False`) são recomendadas para evitar exibir nomes falsos na vitrine da Marina.

## Reprodutibilidade
- Script Python (Unificação, Pivot e Cosseno via Numpy): `07_questionarios_subanalises/scripts/q07_sistema_recomendacao.py`
