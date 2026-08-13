import zipfile
import os

zip_filename = r"E:\repo\lh_nautical_analise\entrega_final_lh_nautical.zip"

files_to_zip = [
    (r"E:\repo\lh_nautical_analise\dashboard.py", "dashboard.py"),
    (r"E:\repo\lh_nautical_analise\README_DASHBOARD.md", "README_DASHBOARD.md"),
    (r"E:\repo\lh_nautical_analise\docs\EXECUTIVE_SUMMARY_V3.pdf", "EXECUTIVE_SUMMARY_LH_NAUTICAL.pdf"),
    (r"E:\repo\lh_nautical_analise\data\processed\fato_vendas.parquet", "data/processed/fato_vendas.parquet"),
    (r"E:\repo\lh_nautical_analise\data\processed\fato_devolucoes.parquet", "data/processed/fato_devolucoes.parquet"),
    (r"E:\repo\lh_nautical_analise\data\processed\dim_clientes.parquet", "data/processed/dim_clientes.parquet"),
    (r"E:\repo\lh_nautical_analise\data\raw\categories.csv", "data/raw/categories.csv")
]

with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for file_path, arcname in files_to_zip:
        if os.path.exists(file_path):
            zipf.write(file_path, arcname)
            print(f"Adicionado: {arcname}")
        else:
            print(f"AVISO: Arquivo não encontrado - {file_path}")

print(f"\\nPacote gerado com sucesso em: {zip_filename}")
