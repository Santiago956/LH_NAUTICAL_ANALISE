# Subanalises Orientadas por Questionarios

Esta pasta centraliza as novas analises que serao elaboradas a partir dos questionarios recebidos ao longo do projeto.

O objetivo e manter a mesma disciplina analitica ja definida para a LH Nautical, mas com uma organizacao voltada a perguntas especificas:

- preservar a pergunta original do questionario;
- mapear qual tema do desafio ela atende;
- declarar metricas e fontes usadas;
- separar fato observado, hipotese e recomendacao;
- registrar limitacoes, premissas e proximos passos;
- manter reprodutibilidade sem alterar os dados brutos em `data/raw/`.

## Relacao com os topicos do desafio

Cada subanalise deve ser classificada em um ou mais topicos:

1. EDA
2. Tratamento e qualidade dos dados
3. Modelagem e analise de vendas
4. Analise de clientes
5. Previsao de demanda
6. Sistema de recomendacao
7. Dashboard ou relatorio executivo

Quando uma pergunta do questionario cruzar mais de um tema, a resposta deve deixar claro qual e o tema principal e quais temas sao secundarios.

## Padrao de resposta esperado

Use o formato F-H-R como padrao executivo:

- **Fato observado:** resultado numerico sustentado pelos dados.
- **Evidencia:** tabela, query, grafico, amostra ou calculo usado.
- **Hipotese:** interpretacao plausivel a partir do cruzamento dos dados.
- **Impacto:** consequencia financeira, operacional ou comercial.
- **Recomendacao:** acao objetiva para o negocio.
- **Limitacao:** ressalvas de dados, granularidade, periodo ou definicao de metrica.

## Estrutura sugerida

```text
07_questionarios_subanalises/
  README.md
  templates/
    subanalise_template.md
  questionarios/
    .gitkeep
  scripts/
    .gitkeep
  notebooks/
    .gitkeep
  outputs/
    .gitkeep
```

## Convencao de nomes

Use nomes curtos, com numero da pergunta e tema:

```text
questionarios/q01_texto_original.md
scripts/q01_nome_da_rotina.py
notebooks/q01_vendas_margem.ipynb
outputs/q01_vendas_margem.md
```

## Fontes preferenciais

- `data/processed/fato_vendas.parquet`
- `data/processed/fato_devolucoes.parquet`
- `data/processed/dim_clientes.parquet`
- CSVs em `data/raw/` apenas quando a pergunta exigir uma entidade ainda nao consolidada.

## Regras de qualidade

- Nao alterar arquivos em `data/raw/`.
- Validar joins antes de concluir resultados.
- Explicitar sinais financeiros: receita, desconto, custo, devolucao, margem e lucro.
- Evitar conclusoes sem evidencia quantitativa.
- Distinguir fato observado de hipotese.
- Em previsao de demanda, manter corte temporal e evitar leakage.
- Em recomendacao, explicar dados considerados e criterio de relacionamento.
