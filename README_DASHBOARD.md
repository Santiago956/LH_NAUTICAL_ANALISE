# Como Executar o Dashboard da LH Nautical

Este pacote contém o Dashboard Interativo (Streamlit) e o Relatório Executivo final (PDF).

## Pré-requisitos
Certifique-se de ter o Python 3.9+ instalado em sua máquina.

## Passo a Passo

1. Extraia todos os arquivos deste `.zip` em uma nova pasta.
2. Abra o terminal (ou Prompt de Comando) e navegue até a pasta extraída.
3. Instale as dependências necessárias executando o comando:
   ```bash
   pip install streamlit duckdb pandas plotly
   ```
4. Execute o dashboard com o comando:
   ```bash
   streamlit run dashboard.py
   ```
5. O dashboard abrirá automaticamente no seu navegador padrão (geralmente no endereço `http://localhost:8501`).

---
**Nota:** O arquivo `EXECUTIVE_SUMMARY_V3.pdf` contém a visão consolidada para leitura rápida e pode ser encaminhado separadamente para a Diretoria.
