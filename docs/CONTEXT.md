# Contexto do Projeto LH Nautical

## Visão Geral
Projeto para resolver o desafio técnico de dados da **LH Nautical**, cobrindo todo o fluxo operacional desde a limpeza dos dados até previsões de vendas e recomendações, visando entregar valor para as áreas de negócios.

## Metodologia Acordada
- **Reprodutibilidade:** Uso de `uv` para gestão de dependências. Scripts organizados modularmente (`src/`, `scripts/`, notebooks nas pastas por etapa).
- **Tratamento Integrado (Fato de Vendas):** Para evitar retrabalho, o tratamento de dados não ocorre isolado apenas no EDA. Criamos uma tabela Fato consolidada (Silver/Gold layer) cruzando dimensões essenciais e realizando cortes lógicos (como o truncamento temporal). Essa base pré-calculada servirá como única fonte da verdade para o EDA profundo, Dashboard e Modelos.
- **Simplicidade (No Black-Box):** Preferência por modelos explicáveis e regras de negócio claras em vez de modelos de deep learning opacos.
- **Validação Temporal Rigorosa:** Como os dados sintéticos vão até o final de 2026 e o período atual (físico) é agosto de 2026, truncamos os dados de vendas para `<= 2026-08-10`. Modelos de previsão usarão "walk-forward validation" para evitar data leakage.
- **Top-Down:** Todas as análises devem partir de uma ótica de negócios, respondendo: o que aconteceu, por que aconteceu, e qual a ação recomendada.

## Descobertas Iniciais (Auditoria de Qualidade)
- **Dados Estruturalmente Limpos:** 0 chaves primárias duplicadas, 0 pedidos com total negativo, 0 variantes vendidas abaixo do preço de custo.
- **Data Leakage:** Identificados pedidos com datas indo até `2026-12-31`. Necessita de corte/tratamento temporal antes da modelagem.
- **Volume:** A base é substancial (e.g., 147k itens de pedido, 115k movimentações de estoque). O uso de `DuckDB` + `Pandas` (ou `Parquet`) foi definido como o padrão para cruzamentos eficientes.

## Principais Descobertas e Ações (Evolução Analítica)
- **Rentabilidade de Produtos:** Constatamos que os Top produtos (Curva A) operam com margens brutas saudáveis (>50%). Não foram identificados "vilões" de rentabilidade (produtos com alta receita e margem base <10%), o que indica que a estratégia primária de precificação e descontos está otimizada.
- **Qualidade de Dados nas Devoluções:** Identificamos severas inconsistências de *input* nos motivos de devolução (erros de digitação, diferenças de maiúsculas). Adotamos uma padronização via `CASE WHEN` no script `02_build_fato_devolucoes.py` para consolidar categorias diretamente na camada Silver/Gold.
- **O Ralo Logístico (Hipóteses Centrais):** A análise das devoluções revelou dois problemas distintos que direcionam ações para times diferentes:
  1. *Fricção Digital:* Desistências, compras duplicadas e divergências de descrição apontam para falhas na interface do e-commerce (falhas na UX do carrinho ou falta de informações claras).
  2. *Fricção Física:* Avarias e defeitos de fábrica escancaram falhas na cadeia logística (controle de qualidade do fornecedor e/ou transportadoras ineficientes).

## Estrutura do Repositório
- `01_eda/` a `06_recomendacao/`: Pastas para os notebooks e scripts executáveis de cada fase do desafio.
- `src/`: Código fonte reutilizável (funções de transformação, etc).
- `scripts/`: Scripts utilitários de execução única (ex: gerador de schemas).
- `docs/`: Documentação, ERD e contextos de negócio.
- `data/raw/`: Arquivos CSV originais (ignorados no git).
- `data/processed/`: Tabelas intermediárias geradas (ex: Fato de Vendas).
