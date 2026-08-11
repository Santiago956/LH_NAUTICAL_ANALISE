# AGENTS.md

## Projeto

Desafio técnico de dados da **LH Nautical**, empresa fictícia de varejo náutico com lojas físicas, armazéns e e-commerce.

Os dados cobrem **2020–2026** e representam o ciclo operacional completo:
- Produtos e catálogo
- Vendas e pedidos
- Pagamentos
- Notas fiscais
- Compras de fornecedores
- Estoque
- Devoluções

Os dados brutos estão em `data/`, contendo **24 arquivos CSV** que representam o schema relacional da empresa.

## Objetivo

Transformar os dados brutos e desorganizados em análises confiáveis e acionáveis, cobrindo todo o fluxo:

1. EDA
2. Tratamento e qualidade dos dados
3. Modelagem e análise de vendas
4. Análise de clientes
5. Previsão de demanda
6. Sistema de recomendação
7. Dashboard/relatório executivo

O foco não é apenas produzir código funcional, mas demonstrar **raciocínio analítico, organização, clareza, qualidade dos dados e geração de valor para o negócio**.

## Stakeholders

### Gabriel Santos — Tech Lead
Prioridades:
- Organização
- Código legível
- Documentação
- Clareza do raciocínio
- Soluções simples e justificáveis
- Reprodutibilidade

Evitar complexidade desnecessária ou soluções "black box".

### Marina Costa — Gerente de Negócios
Prioridades:
- Vendas
- Margem e lucro
- Performance de produtos
- Performance de clientes
- Insights acionáveis

As análises devem responder claramente: **o que aconteceu, por que aconteceu e o que pode ser feito.**

### Sr. Almir — Fundador
Perfil tradicional e cético em relação à tecnologia/cloud.

Apresentar resultados de forma:
- Clara
- Objetiva
- Baseada em evidências
- Orientada a impacto financeiro e operacional

Evitar jargão técnico quando o público for executivo.

## Princípios de Trabalho

- Sempre explorar os dados antes de assumir regras ou padrões.
- Validar schema, tipos, chaves e relacionamentos antes das análises.
- Identificar valores nulos, duplicidades, inconsistências e outliers.
- Documentar decisões de limpeza e transformação.
- Não alterar dados brutos.
- Priorizar soluções simples, transparentes e reproduzíveis.
- Não mascarar problemas de qualidade dos dados.
- Diferenciar claramente **fato observado**, **hipótese** e **recomendação**.
- Toda métrica deve ter sua definição e lógica de cálculo claras.
- Resultados financeiros devem ser tratados com atenção especial a sinais, custos, receitas, descontos, devoluções e margem.

## Análises

As respostas devem ser construídas a partir dos dados reais disponíveis, e não de suposições.

Para cada análise relevante, procurar responder:

1. Qual é o resultado?
2. Qual é a evidência nos dados?
3. Quais fatores explicam o resultado?
4. Qual o impacto para o negócio?
5. Existe alguma limitação ou ressalva?

### Previsão de demanda

Considerar:
- Histórico temporal
- Sazonalidade
- Tendências
- Granularidade adequada
- Validação temporal
- Métricas de avaliação apropriadas

Evitar leakage temporal.

### Recomendação

Explicar:
- Estratégia utilizada
- Dados considerados
- Critério de similaridade/relacionamento
- Limitações
- Como o sistema poderia ser utilizado pelo negócio

## Dashboard / Entrega Final

O dashboard deve comunicar os principais resultados do desafio para um público de negócio.

Visuais sugeridos:
- Ranking/distribuição de prejuízos por produto
- Clientes com maior lucro acumulado
- Vendas médias por dia da semana, incluindo dias sem venda
- Outros insights relevantes identificados durante a análise

Priorizar visualizações que permitam responder rapidamente:
- Onde estamos perdendo dinheiro?
- Quais produtos performam melhor/pior?
- Quais clientes geram mais valor?
- Como as vendas se comportam ao longo do tempo?
- O que merece atenção da gestão?

## Qualidade da Entrega

Antes de finalizar:

- Verificar se todas as questões do desafio foram respondidas.
- Validar cálculos e agregações.
- Conferir joins e possíveis duplicações.
- Garantir consistência entre análises e dashboard.
- Registrar premissas importantes.
- Manter notebooks/scripts organizados e reproduzíveis.
- Não deixar análises sem interpretação de negócio.
- Preferir conclusões sustentadas pelos dados a conclusões especulativas.