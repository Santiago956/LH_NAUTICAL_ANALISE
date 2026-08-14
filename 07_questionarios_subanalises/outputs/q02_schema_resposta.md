# Questao 2 - Schema

## Script

O script foi criado em:

```text
07_questionarios_subanalises/scripts/q02_generate_schema_sql.py
```

Ele utiliza apenas bibliotecas padrao do Python 3:

- `argparse`
- `csv`
- `datetime`
- `os`
- `re`

## Como executar

```bash
python 07_questionarios_subanalises/scripts/q02_generate_schema_sql.py --input-dir data/raw --output schema.sql
```

## O que o script faz

- Le todos os arquivos `.csv` do diretorio informado.
- Usa o nome de cada arquivo como nome da tabela.
- Usa o cabecalho de cada CSV como lista de colunas.
- Normaliza nomes para identificadores compativeis com PostgreSQL.
- Organiza o fluxo em funcoes com nomes proximos ao enunciado, como:
  - `gerar_schema_sql`
  - `ler_csv_e_inferir_colunas`
  - `montar_create_table`
- Infere tipos simples a partir dos valores observados:
  - `BOOLEAN`
  - `INTEGER`
  - `NUMERIC(precision, scale)`
  - `TIMESTAMP`
  - `DATE`
  - `TEXT`
- Gera um unico arquivo `schema.sql` com um `CREATE TABLE IF NOT EXISTS` por CSV.

## Observacao

A inferencia de tipos e uma proposta inicial de schema baseada nos CSVs. Antes de carga produtiva, ainda e recomendavel revisar chaves primarias, chaves estrangeiras, restricoes `NOT NULL` e indices, pois esses elementos dependem de regras de negocio e relacionamentos entre tabelas.

Campos identificadores como `cpf`, `tax_id`, `postal_code` e `phone` sao mantidos como `TEXT`, mesmo quando possuem apenas digitos, para evitar perda de zeros a esquerda ou formatacao.
