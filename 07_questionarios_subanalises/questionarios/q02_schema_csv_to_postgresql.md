# Questao 2 - Schema

## Cenario

A empresa fornecedora do ERP nao permite conexao direta com o banco de dados. A unica forma de obter os dados e pelos CSVs fornecidos.

Para as proximas etapas, os dados precisam ser carregados em um banco de dados. Antes disso, e necessario definir o schema.

## Restricoes

- Considerar todos os CSV como arquivos de fonte.
- Usar obrigatoriamente Python 3.
- Usar somente bibliotecas padrao do Python 3.
- Nao usar pandas, dask, polars ou bibliotecas similares.
- Considerar PostgreSQL como banco de destino.

## Tarefa

Criar um script Python que leia os CSVs de um diretorio e gere um unico arquivo `schema.sql` com as instrucoes `CREATE TABLE` para cada CSV.
