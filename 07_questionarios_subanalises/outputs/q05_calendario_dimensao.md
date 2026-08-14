# Questao 5 - Dimensao de calendario

## Pergunta original

> Qual e o dia da semana, nas lojas fisicas, temos a pior media de vendas? (para decidir se vale a pena fechar a loja nesses dias).

## Tema do desafio

- Tema principal: Modelagem e analise de vendas (item 3).
- Temas secundarios: Dashboard ou relatorio executivo (item 7) e Tratamento e qualidade dos dados (item 2), pois o resultado alimenta o visual "vendas medias por dia da semana, incluindo dias sem venda" e exige preencher dias sem registro com zero.
- Stakeholder principal: Sr. Almir (decisao de abrir/fechar loja) e Marina Costa (performance de vendas).

## Objetivo de negocio

Decidir se vale a pena fechar a loja fisica no dia da semana de pior media, usando uma metrica correta que nao seja inflada pela ausencia de dias sem venda na tabela `orders`.

## Dados e metricas

### Fontes

- `data/raw/orders.csv` (colunas `created_at`, `channel`, `total`). Dados brutos nao alterados.

### Metricas

| Metrica | Definicao | Observacoes |
| --- | --- | --- |
| Vendas diarias | `SUM(total)` por dia para `channel = 'pos'` | Soma de valor da venda por dia |
| Media por dia da semana | `AVG` das vendas diarias considerando TODOS os dias do calendario | Dias sem venda entram com valor 0 |
| Dias sem venda | Dias do calendario cujo valor diario e 0 | Loja aberta porem sem venda registrada |
| Media apenas dias com venda | `AVG` das vendas diarias ignorando dias zerados | Versao "inflada" usada pelo estagiario |

## Validacoes antes da analise

- [x] Periodo analisado segue a premissa (menor a maior data de venda no arquivo: 2020-01-01 a 2026-12-31).
- [x] Chaves e joins validados: `created_at::date` entre calendario e vendas; 0 duplicidades de `orders.id` (auditoria do projeto).
- [x] Duplicidades relevantes checadas: uma linha por dia no calendario (2557 dias).
- [x] Nulos tratados: dias sem venda convertidos para 0 via `COALESCE`.
- [x] Sinais financeiros conferidos: soma de `total` por dia, apenas canal `pos`.

## Resultado

### Fato observado

O pior dia da semana em lojas fisicas e a **Quinta-feira**, com media de **R$ 157.154,32 por dia** no periodo, incluindo os dias sem venda. O Domingo, apontado como "otimo" pelo estagiario, e na verdade o segundo pior dia (R$ 157.616,13).

### Evidencia nos dados

| dia_semana | dias_no_periodo | dias_sem_venda | vendas_totais | media_vendas_por_dia |
| ---: | ---: | ---: | ---: | ---: |
| Quinta-feira | 366 | 20 | 57.518.480,61 | 157.154,32 |
| Domingo | 365 | 12 | 57.529.887,95 | 157.616,13 |
| Segunda-feira | 365 | 7 | 57.758.021,43 | 158.241,15 |
| Sabado | 365 | 11 | 60.173.268,58 | 164.858,27 |
| Terca-feira | 365 | 8 | 60.633.373,26 | 166.118,83 |
| Sexta-feira | 365 | 10 | 62.120.694,25 | 170.193,68 |
| Quarta-feira | 366 | 10 | 63.539.589,22 | 173.605,44 |

Comparativo do erro do estagiario (media apenas nos dias com venda vs. media corrigida):

| dia_semana | media apenas dias com venda | media corrigida (inclui zeros) | inflacao |
| ---: | ---: | ---: | ---: |
| Domingo | 162.974,19 | 157.616,13 | +3,4% |
| Quinta-feira | 166.238,38 | 157.154,32 | +5,8% |

### Hipotese

A distorcao acontece porque o estagiario calculou a media apenas sobre os dias com venda registrada. Como a loja abre todos os dias, mas em alguns dias nao registra venda (20 quintas e 12 domingos no periodo), esses dias sumiram do calculo e inflaram a media dos dias "cheios". No ranking corrigido, a Quinta-feira e o dia mais fraco — possivelmente por combinacao de menor fluxo de clientes no meio da semana e ausencia de campanhas nesse dia —, hipotese que so pode ser confirmada cruzando com localidade, canal e promocoes.

### Impacto para o negocio

- Fechar a loja na Quinta-feira eliminaria, em media, **R$ 157 mil/dia** de receita nas lojas fisicas, sem garantia de economia equivalente. A diferenca entre o pior e o melhor dia e de apenas ~10% (R$ 16,4 mil/dia), entao **fechar nao encontra suporte nos dados**.
- Se o erro do estagiario fosse replicado no dashboard, o ranking de dias da semana ficaria distorcido e levaria a decisoes erradas (ex: priorizar Domingo).

### Recomendacao

1. Nao fechar a loja: a Quinta-feira continua sendo um dia de receita relevante; a diferenca para os demais dias nao justifica a perda.
2. Tratar o dia fraco como oportunidade: usar quintas para manutencao, treinamento e promocoes direcionadas (ex: "quinta do nautico") para elevar a media.
3. Adotar a dimensao de calendario no pipeline/dashboard: qualquer analise de venda por dia da semana deve preencher dias sem venda com zero (requisito do AGENTS.md).
4. Investigar a causa da fraqueza da Quinta-feira cruzando com devolucoes, localidades e campanhas antes de qualquer mudanca operacional.

### Limitacoes e ressalvas

- O periodo segue a premissa da questao (menor a maior data do arquivo), chegando a 2026-12-31, ou seja, ha datas futuras ao momento fisico atual (ago/2026) — data leakage conhecido do projeto. Teste de sensibilidade truncando em 2026-08-10 mantem a Quinta-feira como pior dia (R$ 142.627,41), indicando robustez.
- A data da venda usada foi `created_at`; validado que `created_at = placed_at` em 100% das linhas.
- As diferencas entre dias (~10%) sao pequenas; recomenda-se intervalo de confianca e analise por localidade para sustentar decisoes de fechamento.

## Reprodutibilidade

- Script de validacao: `07_questionarios_subanalises/scripts/q05_validar_calendario_duckdb.py`
- SQL de entrega: `07_questionarios_subanalises/outputs/q05_calendario_dimensao.sql`
- Tabelas intermediarias: `dim_data`, `vendas_diarias_pos`, `calendario_vendas` (criadas pelo SQL)
- Outputs gerados: tabela de medias por dia da semana acima

## Status

- [x] Pergunta recebida
- [x] Dados mapeados
- [x] Analise executada
- [x] Resultado validado
- [x] Interpretacao de negocio escrita
- [ ] Pronto para consolidacao no dashboard ou relatorio