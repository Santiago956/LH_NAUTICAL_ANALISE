# Framework Analítico e Tomada de Decisão

Como este projeto integra um processo seletivo, este documento visa cristalizar a **lógica de raciocínio** e a **metodologia de tomada de decisão** aplicadas em toda a construção das análises para a LH Nautical. 

O foco não é apenas a proficiência em engenharia ou ciência de dados, mas sim a capacidade de gerar **Inteligência de Negócios (BI) acionável**, equilibrando o rigor técnico exigido pelo Tech Lead (Gabriel) com o pragmatismo focado em lucro exigido pela Diretoria (Sr. Almir e Marina).

---

## 1. Abordagem Top-Down (Orientação a Valor)
Não fazemos exploração de dados sem um alvo de negócio. O trabalho obedece a hierarquia:
1. **Diagnóstico Financeiro:** Onde estamos perdendo dinheiro? (Rupturas, devoluções, margem negativa).
2. **Otimização:** Quais alavancas de lucro (produtos curva A, clientes de alto LTV) podemos potencializar?
3. **Predição e IA:** Apenas quando as regras descritivas já geraram valor, aplicamos modelos complexos (Previsão de Demanda e Sistemas de Recomendação) — e mesmo assim, mantendo a interpretabilidade (evitando "caixas pretas").

## 2. Padrão de Comunicação de Insights (F-H-R)
Para contornar o ceticismo com a área de dados e evitar jargões técnicos na camada executiva, todo insight descoberto nos notebooks e painéis será documentado no seguinte formato:

1. **Fato Observado:** A evidência numérica incontestável nos dados tratados.
   * *Exemplo: "O SKU X representa 15% do volume de vendas, mas sua margem bruta é inferior a 3%."*
2. **Hipótese:** A causa estrutural baseada no cruzamento de dimensões (ex: Vendas cruzado com Logística).
   * *Exemplo: "A margem é corroída por descontos excessivos aplicados sistematicamente na Loja Z."*
3. **Recomendação:** Ação focada no negócio.
   * *Exemplo: "Revisar imediatamente as alçadas de descontos para a Loja Z na categoria de caiaques."*

## 3. Roadmap da Análise de Negócios
Nosso fluxo de trabalho nas etapas 03 a 06 seguirá o pipeline:
- **Etapa A (Produtos e Canais):** Curva ABC, identificação de heróis e vilões de margem.
- **Etapa B (Eficiência):** Integração dos dados de **Devolução (`returns`)**, quantificando o ralo logístico.
- **Etapa C (Clientes):** Clusterização B2B vs B2C, ranqueamento de LTV.
- **Etapa D (Preditivo):** Forecast de Demanda rigoroso (com proteção contra *Data Leakage*) para otimizar alocação de compras da lh nautical.
