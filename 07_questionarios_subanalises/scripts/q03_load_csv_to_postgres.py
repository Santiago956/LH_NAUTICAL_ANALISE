"""
Questao 3 - Carregamento

Carrega todos os arquivos CSV em um banco PostgreSQL, respeitando o schema
criado na Questao 2.

Regras atendidas:
- usa Python 3;
- carrega todos os CSVs de um diretorio;
- executa o schema.sql antes da carga;
- nao remove nulos;
- nao corrige caracteres especiais;
- nao altera os arquivos CSV de origem.

Dependencia externa:
    pip install psycopg2-binary
"""

import argparse
import os
import re

import psycopg2


def normalizar_nome_sql(nome_original):
    """Mantem a mesma regra de nome de tabela usada na Questao 2."""
    nome = re.sub(r"[^a-zA-Z0-9_]+", "_", nome_original.strip().lower())
    nome = re.sub(r"_+", "_", nome).strip("_")

    if not nome:
        nome = "coluna"

    if nome[0].isdigit():
        nome = f"col_{nome}"

    return nome


def listar_csvs(diretorio_csv):
    """Lista todos os arquivos CSV que serao carregados."""
    return sorted(
        arquivo for arquivo in os.listdir(diretorio_csv) if arquivo.lower().endswith(".csv")
    )


def executar_schema(conexao, arquivo_schema):
    """Executa o arquivo schema.sql gerado na Questao 2."""
    with open(arquivo_schema, "r", encoding="utf-8") as arquivo_sql:
        sql = arquivo_sql.read()

    with conexao.cursor() as cursor:
        cursor.execute(sql)


def truncar_tabelas(conexao, diretorio_csv):
    """Opcional: limpa as tabelas antes da carga para evitar duplicidade."""
    arquivos_csv = listar_csvs(diretorio_csv)
    tabelas = [
        normalizar_nome_sql(os.path.splitext(arquivo_csv)[0])
        for arquivo_csv in arquivos_csv
    ]

    if not tabelas:
        return

    comando = "TRUNCATE TABLE " + ", ".join(tabelas) + " RESTART IDENTITY;"

    with conexao.cursor() as cursor:
        cursor.execute(comando)


def carregar_csv(conexao, caminho_csv, nome_tabela):
    """Carrega um CSV na tabela PostgreSQL correspondente usando COPY."""
    comando_copy = f"""
        COPY {nome_tabela}
        FROM STDIN
        WITH (
            FORMAT CSV,
            HEADER TRUE,
            DELIMITER ',',
            QUOTE '"',
            NULL ''
        )
    """

    with conexao.cursor() as cursor:
        with open(caminho_csv, "r", encoding="utf-8", newline="") as arquivo_csv:
            cursor.copy_expert(comando_copy, arquivo_csv)


def carregar_todos_csvs(conexao, diretorio_csv):
    """Carrega todos os CSVs do diretorio informado."""
    arquivos_csv = listar_csvs(diretorio_csv)

    for arquivo_csv in arquivos_csv:
        caminho_csv = os.path.join(diretorio_csv, arquivo_csv)
        nome_tabela = normalizar_nome_sql(os.path.splitext(arquivo_csv)[0])

        print(f"Carregando {arquivo_csv} -> tabela {nome_tabela}")
        carregar_csv(conexao, caminho_csv, nome_tabela)


def abrir_conexao(args):
    """Abre conexao com PostgreSQL usando argumentos ou variaveis de ambiente."""
    return psycopg2.connect(
        host=args.host or os.getenv("PGHOST", "localhost"),
        port=args.port or os.getenv("PGPORT", "5432"),
        dbname=args.database or os.getenv("PGDATABASE"),
        user=args.user or os.getenv("PGUSER"),
        password=args.password or os.getenv("PGPASSWORD"),
    )


def main():
    parser = argparse.ArgumentParser(
        description="Carrega todos os CSVs em PostgreSQL respeitando o schema.sql."
    )
    parser.add_argument(
        "--input-dir",
        default=os.path.join("data", "raw"),
        help="Diretorio onde estao os CSVs. Padrao: data/raw",
    )
    parser.add_argument(
        "--schema-file",
        default="schema.sql",
        help="Arquivo schema.sql criado na Questao 2. Padrao: schema.sql",
    )
    parser.add_argument("--host", help="Host do PostgreSQL. Padrao: PGHOST ou localhost")
    parser.add_argument("--port", help="Porta do PostgreSQL. Padrao: PGPORT ou 5432")
    parser.add_argument("--database", help="Nome do banco. Padrao: PGDATABASE")
    parser.add_argument("--user", help="Usuario. Padrao: PGUSER")
    parser.add_argument("--password", help="Senha. Padrao: PGPASSWORD")
    parser.add_argument(
        "--truncate",
        action="store_true",
        help="Limpa as tabelas antes da carga. Use apenas se quiser recarregar tudo.",
    )
    args = parser.parse_args()

    conexao = abrir_conexao(args)

    try:
        executar_schema(conexao, args.schema_file)

        if args.truncate:
            truncar_tabelas(conexao, args.input_dir)

        carregar_todos_csvs(conexao, args.input_dir)
        conexao.commit()
        print("Carga finalizada com sucesso.")
    except Exception:
        conexao.rollback()
        raise
    finally:
        conexao.close()


if __name__ == "__main__":
    main()
