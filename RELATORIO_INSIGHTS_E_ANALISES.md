# Relatório Executivo Analítico - LH Nautical ⚓
**Desafio Técnico de Dados - 2020 a 2026**

Este documento sumariza os achados mais críticos extraídos das tabelas modeladas de Vendas, Devoluções e Clientes da LH Nautical. Ele serve como complemento interpretativo ao Dashboard interativo e consolida respostas acionáveis para o corpo executivo.

---

## 1. Visão Geral do Faturamento e Perdas
Durante o período analisado (2020 - 2026), a LH Nautical apresentou fortes resultados comerciais, mas gargalos logísticos e de inventário seguem minando o lucro líquido da companhia.

* **Faturamento Bruto Total:** ~R$ 1,31 Bilhão
* **Total Perdido em Devoluções:** ~R$ 5,4 Milhões
* **Cliente Mais Valioso (LTV):** Clarice Moura (com mais de R$ 1,28 Milhão em faturamento acumulado). A retenção dessa fatia hiper-lucrativa (Curva A) é mandatória.

---

## 2. O Ralo Financeiro das Devoluções (Onde estamos perdendo dinheiro?)
As devoluções não afetam os produtos de forma igual. Alguns produtos específicos estão drenando sistematicamente a margem de lucro.
* **O Maior Ofensor:** A **"Bússola de Bordo 8282"** liderou o volume financeiro de estornos (mais de R$ 58 mil perdidos apenas neste SKU).
* **Insight de Negócio:** Produtos com alto índice de retorno crônico geralmente possuem descrições enganosas no E-commerce, manuais complexos ou defeitos de lote no fabricante. 
* **Ação Recomendada:** Pausar temporariamente as campanhas de marketing para a "Bússola 8282", auditar o fornecedor desse lote e revisar a clareza da página de vendas no site.

---

## 3. O Dia da Semana: Fechar ou não fechar?
Foi levantada a hipótese de fechamento de lojas físicas nos piores dias de venda. Uma análise amadora (ignorando os dias em que a loja abriu mas vendeu zero) apontou erroneamente o Domingo como o melhor dia.
* **O Fato:** O verdadeiro pior dia do varejo físico é a **Quinta-feira** (Média: R$ 157.154,32/dia e 20 dias zerados ao longo do histórico).
* **Decisão:** A diferença de faturamento para os outros dias (cerca de 10%) não sustenta matematicamente o fechamento das portas.
* **Ação Recomendada:** Manter a loja aberta. Otimizar a Quinta-feira com promoções pontuais ("Quinta do Marinheiro") ou utilizá-la estrategicamente para manutenção, balanço de estoque e treinamento da equipe comercial.

---

## 4. O Risco da Previsão de Demanda Estática (Verão 2026)
O histórico recente demonstrou rupturas catastróficas de estoque no Verão (Falta de Coletes Salva-Vidas). Para evitar isso, analisamos um baseline estatístico sugerido (Média Móvel de 3 meses) projetando o estoque da "Bússola de Bordo 702".
* **O Fato:** O modelo errou por uma margem inaceitável de **~30 unidades por mês** (MAE = 30.38). Em Janeiro/2026, ele previu vendas de 33 unidades, mas a demanda real explodiu para 77 unidades.
* **Por que isso acontece:** Médias Móveis curtas ignoram completamente a "Sazonalidade Anual". O modelo calculou o volume do Verão usando o fluxo ameno da Primavera.
* **Ação Recomendada:** Abandonar o *feeling* é o caminho certo, mas a Média Móvel é perigosa para produtos náuticos de verão. Recomenda-se a implementação imediata de algoritmos sensíveis à sazonalidade (ex: Prophet ou Auto-ARIMA) para as compras de Q4 e Q1.

---

## 5. Estratégia de Cross-Selling (Motor de Recomendação)
Muitos clientes esqueciam de comprar defensas para suas lanchas. Desenvolvemos uma inteligência de "Quem comprou X, também levou Y", calculando o *Cosseno de Similaridade* do comportamento dos usuários sem a necessidade de tecnologias pesadas e custosas.
* **Teste Prático:** Clientes que compram o *"Motor de Popa 1949"* demonstraram uma correlação gravíssima de comportamento conjunto com a *"Vela Mestra 1913"* e com o *"Cabo Náutico 2105"*. 
* **Alerta de Qualidade de Dados:** O motor identificou um produto de teste ("asdf") sendo comprado em produção. 
* **Ação Recomendada:** Ativar a vitrine baseada no algoritmo nas páginas de *Checkout* do site e expurgar/desativar produtos de teste da base.

---
**Nota Técnica aos Revisores (Engenharia e Dados):** 
A pipeline inteira que sustenta estes achados (desde os scripts de modelagem do Data Warehouse `data/processed`, o *Cosine Similarity* construído em Numpy matricial puro, e a limpeza temporal via `COALESCE` com *DuckDB* para evitar o mascaramento de dias zerados) está estruturada e empacotada na pasta do repositório para total reprodutibilidade local.
