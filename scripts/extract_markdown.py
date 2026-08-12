import json
import os

notebooks = [
    r"E:\repo\lh_nautical_analise\03_analise_vendas\01_rentabilidade_produtos.ipynb",
    r"E:\repo\lh_nautical_analise\03_analise_vendas\02_analise_devolucoes.ipynb"
]

output = []
for nb_path in notebooks:
    output.append(f"\n{'='*50}\nNotebook: {nb_path}\n{'='*50}")
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for cell in nb.get('cells', []):
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                output.append(source)
                output.append('-'*40)
    except Exception as e:
        output.append(f"Error reading {nb_path}: {e}")

with open(r"E:\repo\lh_nautical_analise\scripts\extracted_markdown.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(output))
