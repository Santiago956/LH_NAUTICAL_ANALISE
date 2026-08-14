# Questao 3 - Carregamento

## Script

O script foi criado em:

```text
07_questionarios_subanalises/scripts/q03_load_csv_to_postgres.py
```

## Dependencia

Como a questao permite bibliotecas externas para conexao e carregamento, o script usa `psycopg2`:

```bash
pip install psycopg2-binary
```

## Como executar

Usando argumentos:

```bash
python 07_questionarios_subanalises/scripts/q03_load_csv_to_postgres.py ^
  --input-dir data/raw ^
  --schema-file schema.sql ^
  --host localhost ^
  --port 5432 ^
  --database lh_nautical ^
  --user postgres ^
  --password sua_senha
```

Ou usando variaveis de ambiente do PostgreSQL:

```bash
set PGHOST=localhost
set PGPORT=5432
set PGDATABASE=lh_nautical
set PGUSER=postgres
set PGPASSWORD=sua_senha

python 07_questionarios_subanalises/scripts/q03_load_csv_to_postgres.py --input-dir data/raw --schema-file schema.sql
```

## O que o script faz

- Abre conexao com PostgreSQL.
- Executa o `schema.sql` criado na Questao 2.
- Lista todos os arquivos `.csv` do diretorio informado.
- Usa o nome de cada CSV como nome da tabela.
- Carrega cada arquivo com `COPY ... FROM STDIN WITH CSV HEADER`.
- Mantem nulos como nulos no banco.
- Nao corrige caracteres especiais.
- Nao altera os arquivos de origem.

## Observacao

O parametro `--truncate` existe apenas para recargas controladas. Sem esse parametro, o script nao apaga dados antes de carregar.
