"""
Questao 2 - Schema

Le todos os arquivos CSV de um diretorio e gera um unico arquivo schema.sql
com instrucoes CREATE TABLE para PostgreSQL.

Regras atendidas:
- usa Python 3;
- usa apenas bibliotecas padrao;
- considera cada CSV como uma tabela;
- usa o cabecalho do CSV como lista de colunas.
"""

import argparse
import csv
import datetime
import os
import re


VALORES_NULOS = {"", "null", "none", "nan", "na", "n/a"}

# Mesmo quando parecem numericos, estes campos devem ser texto:
# podem conter zeros a esquerda ou caracteres de formatacao.
COLUNAS_IDENTIFICADORAS_COMO_TEXTO = {
    "cpf",
    "cnpj",
    "tax_id",
    "state_registration",
    "postal_code",
    "phone",
}


def normalizar_nome_sql(nome_original):
    """Transforma nomes de arquivos e colunas em identificadores simples de SQL."""
    nome = re.sub(r"[^a-zA-Z0-9_]+", "_", nome_original.strip().lower())
    nome = re.sub(r"_+", "_", nome).strip("_")

    if not nome:
        nome = "coluna"

    if nome[0].isdigit():
        nome = f"col_{nome}"

    return nome


def normalizar_colunas(cabecalho):
    """Normaliza nomes de colunas e evita nomes duplicados."""
    nomes_usados = {}
    colunas = []

    for coluna_original in cabecalho:
        nome_base = normalizar_nome_sql(coluna_original)
        quantidade = nomes_usados.get(nome_base, 0)
        nomes_usados[nome_base] = quantidade + 1

        if quantidade == 0:
            colunas.append(nome_base)
        else:
            colunas.append(f"{nome_base}_{quantidade + 1}")

    return colunas


def criar_perfil_coluna():
    """Perfil usado para inferir o tipo PostgreSQL de cada coluna."""
    return {
        "tem_valor": False,
        "booleano": True,
        "inteiro": True,
        "decimal": True,
        "data": True,
        "data_hora": True,
        "digitos_inteiros": 0,
        "casas_decimais": 0,
    }


def eh_nulo(valor):
    return valor is None or valor.strip().lower() in VALORES_NULOS


def eh_booleano(valor):
    return valor.strip().lower() in {"true", "false", "t", "f", "yes", "no", "y", "n"}


def eh_inteiro(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False


def eh_decimal(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False


def eh_data(valor):
    try:
        datetime.date.fromisoformat(valor)
        return True
    except ValueError:
        return False


def eh_data_hora(valor):
    try:
        datetime.datetime.fromisoformat(valor.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def contar_digitos_decimal(valor):
    texto = valor.strip()

    if texto.startswith(("+", "-")):
        texto = texto[1:]

    if "." in texto:
        parte_inteira, parte_decimal = texto.split(".", 1)
    else:
        parte_inteira, parte_decimal = texto, ""

    digitos_inteiros = len(parte_inteira.lstrip("0"))
    casas_decimais = len(parte_decimal.rstrip("0"))

    return digitos_inteiros, casas_decimais


def atualizar_perfil_coluna(perfil, valor):
    """Atualiza o perfil da coluna a partir de um valor observado no CSV."""
    if eh_nulo(valor):
        return

    perfil["tem_valor"] = True
    perfil["booleano"] = perfil["booleano"] and eh_booleano(valor)
    perfil["inteiro"] = perfil["inteiro"] and eh_inteiro(valor)
    perfil["decimal"] = perfil["decimal"] and eh_decimal(valor)
    perfil["data"] = perfil["data"] and eh_data(valor)
    perfil["data_hora"] = perfil["data_hora"] and eh_data_hora(valor)

    if eh_decimal(valor):
        digitos_inteiros, casas_decimais = contar_digitos_decimal(valor)
        perfil["digitos_inteiros"] = max(perfil["digitos_inteiros"], digitos_inteiros)
        perfil["casas_decimais"] = max(perfil["casas_decimais"], casas_decimais)


def inferir_tipo_postgresql(nome_coluna, perfil):
    """Converte o perfil observado da coluna em um tipo PostgreSQL."""
    if not perfil["tem_valor"]:
        return "TEXT"

    if nome_coluna in COLUNAS_IDENTIFICADORAS_COMO_TEXTO or nome_coluna.endswith("_code"):
        return "TEXT"

    if perfil["booleano"]:
        return "BOOLEAN"

    if perfil["inteiro"]:
        return "INTEGER"

    if perfil["decimal"]:
        precisao = perfil["digitos_inteiros"] + perfil["casas_decimais"]
        escala = perfil["casas_decimais"]
        return f"NUMERIC({max(precisao, 1)}, {escala})"

    if perfil["data_hora"]:
        return "TIMESTAMP"

    if perfil["data"]:
        return "DATE"

    return "TEXT"


def ler_csv_e_inferir_colunas(caminho_csv):
    """Le um CSV e devolve os nomes das colunas e seus tipos inferidos."""
    with open(caminho_csv, "r", encoding="utf-8", newline="") as arquivo_csv:
        leitor = csv.reader(arquivo_csv)
        cabecalho = next(leitor)
        colunas = normalizar_colunas(cabecalho)
        perfis = [criar_perfil_coluna() for _ in colunas]

        for linha in leitor:
            for indice, perfil in enumerate(perfis):
                valor = linha[indice] if indice < len(linha) else ""
                atualizar_perfil_coluna(perfil, valor)

    tipos = [inferir_tipo_postgresql(coluna, perfil) for coluna, perfil in zip(colunas, perfis)]
    return colunas, tipos


def montar_create_table(nome_tabela, colunas, tipos):
    """Monta a instrucao CREATE TABLE de uma tabela."""
    definicoes_colunas = []

    for coluna, tipo in zip(colunas, tipos):
        definicoes_colunas.append(f"    {coluna} {tipo}")

    return (
        f"CREATE TABLE IF NOT EXISTS {nome_tabela} (\n"
        + ",\n".join(definicoes_colunas)
        + "\n);"
    )


def gerar_schema_sql(diretorio_csv, arquivo_saida):
    """Gera o arquivo final schema.sql a partir de todos os CSVs do diretorio."""
    arquivos_csv = sorted(
        arquivo for arquivo in os.listdir(diretorio_csv) if arquivo.lower().endswith(".csv")
    )

    comandos_sql = [
        "-- Schema gerado automaticamente a partir dos arquivos CSV.",
        "-- Banco de destino: PostgreSQL.",
        "-- Script gerado usando apenas bibliotecas padrao do Python 3.",
        "",
    ]

    for arquivo_csv in arquivos_csv:
        caminho_csv = os.path.join(diretorio_csv, arquivo_csv)
        nome_tabela = normalizar_nome_sql(os.path.splitext(arquivo_csv)[0])
        colunas, tipos = ler_csv_e_inferir_colunas(caminho_csv)

        comandos_sql.append(f"-- Arquivo fonte: {arquivo_csv}")
        comandos_sql.append(montar_create_table(nome_tabela, colunas, tipos))
        comandos_sql.append("")

    with open(arquivo_saida, "w", encoding="utf-8", newline="\n") as arquivo_sql:
        arquivo_sql.write("\n".join(comandos_sql))


def main():
    parser = argparse.ArgumentParser(
        description="Gera um schema.sql PostgreSQL a partir de arquivos CSV."
    )
    parser.add_argument(
        "--input-dir",
        default=os.path.join("data", "raw"),
        help="Diretorio onde estao os CSVs. Padrao: data/raw",
    )
    parser.add_argument(
        "--output",
        default="schema.sql",
        help="Arquivo SQL de saida. Padrao: schema.sql",
    )
    args = parser.parse_args()

    gerar_schema_sql(args.input_dir, args.output)


if __name__ == "__main__":
    main()
