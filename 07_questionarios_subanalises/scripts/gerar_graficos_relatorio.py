import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

def main():
    out_dir = '07_questionarios_subanalises/outputs/imagens'
    os.makedirs(out_dir, exist_ok=True)
    
    # 1. Gráfico da Questão 5
    dias = ['Quinta-feira', 'Domingo', 'Segunda-feira', 'Sábado', 'Terça-feira', 'Sexta-feira', 'Quarta-feira']
    valores = [157154.32, 157616.13, 158241.15, 164858.27, 166118.83, 170193.68, 173605.44]
    
    plt.figure(figsize=(10, 6))
    colors = ['#e74c3c' if d == 'Quinta-feira' else '#3498db' for d in dias]
    ax = sns.barplot(x=dias, y=valores, palette=colors)
    plt.title('Média de Vendas Diárias (Lojas Físicas) por Dia da Semana', fontsize=14)
    plt.ylabel('Faturamento Médio (R$)', fontsize=12)
    plt.xlabel('Dia da Semana', fontsize=12)
    plt.ylim(150000, 180000)
    plt.xticks(rotation=45)
    
    for i, v in enumerate(valores):
        ax.text(i, v + 500, f'R$ {v:,.0f}', ha='center', fontsize=9)
        
    plt.tight_layout()
    plt.savefig(f'{out_dir}/q5_dias.png', dpi=300)
    plt.close()
    
    # 2. Gráfico da Questão 6
    meses = ['Out/25', 'Nov/25', 'Dez/25', 'Jan/26', 'Fev/26', 'Mar/26']
    vendas_reais = [25, 54, 19, 77, 57, 54]
    vendas_previstas = [np.nan, np.nan, np.nan, 32.67, 35.22, 28.96]
    
    plt.figure(figsize=(10, 6))
    plt.plot(meses, vendas_reais, marker='o', label='Vendas Reais', color='#2ecc71', linewidth=2.5)
    plt.plot(meses, vendas_previstas, marker='X', linestyle='--', label='Previsão (Baseline: Média Móvel)', color='#e74c3c', linewidth=2.5, markersize=8)
    
    plt.title('Bússola de Bordo 702: Vendas Reais vs Previsão (Média Móvel)', fontsize=14)
    plt.ylabel('Unidades Vendidas', fontsize=12)
    plt.xlabel('Mês', fontsize=12)
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    
    # Shade Q1 2026
    plt.axvspan('Jan/26', 'Mar/26', color='gray', alpha=0.1, label='Período de Teste (Q1 26)')
    
    plt.tight_layout()
    plt.savefig(f'{out_dir}/q6_previsao.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    main()
