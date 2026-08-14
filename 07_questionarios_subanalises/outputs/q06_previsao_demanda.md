# Questão 6 - Previsão de demanda

## Pergunta original
O baseline é adequado para esse produto? Cite uma limitação desse método.

## Tema do desafio
- Tema principal: Previsão de demanda (item 5).
- Tema secundário: Modelagem e análise de vendas (item 3).
- Stakeholders principais: Sr. Almir e Gabriel Santos (Tech Lead).

## Objetivo de negócio
Evitar rupturas de estoque no verão e excesso de compras através da previsão acurada de demanda, abandonando o "feeling" na tomada de decisão.

## Dados e Métricas
- **Dataset unificado**: Cruzamento de `products`, `product_variants`, `orders` e `order_items`.
- **Baseline**: Média móvel dos últimos 3 meses de vendas calculada de forma iterativa (*multi-step ahead*).
- **Métrica de Avaliação**: MAE (Mean Absolute Error).

## Resultado

### 1 e 2. Unificação dos Datasets e Modelo Baseline
Foi construído um modelo preditivo calculando iterativamente a média móvel. Para o primeiro trimestre de 2026:
- **Janeiro**: usou a média real de Outubro, Novembro e Dezembro de 2025.
- **Fevereiro**: usou a média de Novembro, Dezembro de 2025 e a previsão gerada de Janeiro.
- **Março**: usou a média de Dezembro de 2025 e as previsões de Janeiro e Fevereiro.

### 3 e 4. Previsões vs. Valores Reais e MAE

| Mês (2026) | Previsão (Baseline) | Valor Real | Erro Absoluto |
| :--- | :--- | :--- | :--- |
| Janeiro | 32,67 | 77 | 44,33 |
| Fevereiro | 35,22 | 57 | 21,78 |
| Março | 28,96 | 54 | 25,04 |

**MAE (Mean Absolute Error):** 30,38

### 5. Respostas Objetivas

**a. O baseline é adequado para esse produto?**
**Não.** O Erro Médio Absoluto (~30 unidades) é gigantesco frente ao volume mensal de vendas do produto (em torno de 50-70 unidades no período). O modelo está subestimando drasticamente a demanda (previu ~33 para janeiro, quando a demanda real foi de 77). Se a empresa utilizasse esse baseline para definir compras, faltaria estoque de "Bússola de Bordo 702" durante todo o verão, resultando em rupturas e vendas perdidas (o que enfureceria o Sr. Almir, como aconteceu com os "Coletes Salva-Vidas").

**b. Cite uma limitação desse método.**
A **incapacidade de capturar sazonalidade e tendências de longo prazo**. A Média Móvel Simples (SMA) possui forte inércia; ao olhar estritamente para o trimestre anterior (Primavera), ela falha em antecipar as fortes vendas sazonais características do Verão (Q1). Além disso, por se tratar de uma previsão em múltiplos passos (*multi-step ahead*), estimativas são usadas como insumo para as estimativas seguintes, acumulando e amplificando os erros das previsões iniciais.

## Reprodutibilidade
- Script Python (Unificação dos CSVs e Modelo): `07_questionarios_subanalises/scripts/q06_previsao_demanda.py`
