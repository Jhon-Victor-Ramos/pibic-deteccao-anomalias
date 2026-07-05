# Detecção de Falhas em Séries Temporais Industriais com Machine Learning

[![Licença: MIT](https://img.shields.io/badge/Licença-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.x](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)

> Repositório oficial com os códigos e recursos desenvolvidos para o *Programa Institucional de Bolsas de Iniciação Científica* (*PIBIC*) da *Universidade Católica de Pernambuco* (*UNICAP*, 2025-2026).

**Orientador:** [Prof. Dr. Wilmer Yecid Córdoba Camacho](http://lattes.cnpq.br/3667425974106334)

---

## Índice
1. [Sobre o Projeto](#sobre-o-projeto)
2. [Arquitetura e Metodologia](#arquitetura-e-metodologia)
3. [Resultados Finais](#resultados-finais)
4. [Estrutura do Repositório](#estrutura-do-repositório)
5. [Como Executar](#como-executar)
6. [Autores](#autores)

---

## Sobre o Projeto

Este trabalho integra o projeto guarda-chuva *"Desenvolvimento de Modelos Computacionais para Reconhecimento de Padrões em Séries Temporais Multivariadas"*. A frente de pesquisa documentada neste repositório foca exclusivamente no setor da **Indústria 4.0**, abordando o desafio da *Manutenção Preditiva*.

O objetivo principal consiste em desenvolver, treinar e validar algoritmos de detecção de anomalias não-supervisionados capazes de identificar falhas iniciais em máquinas rotativas (como rolamentos, por exemplo) a partir de sinais de vibração, garantindo viabilidade computacional para futura implementação com *Edge Computing* (ex: *Raspberry Pi*).

---

## Arquitetura e Metodologia

Para garantir o rigor na avaliação do modelo, a pesquisa utilizou o dataset da ***Case Western Reserve University (CWRU)***, focando nos sinais do acelerômetro *Drive End* (12 kHz) operando sob carga constante (0 HP). O fluxo de trabalho de dados foi estruturado nas seguintes etapas:

1. **Extração de Características:** Divisão do sinal bruto de vibração em janelas temporais fixas ($1024$ amostras) e cálculo de métricas estatísticas de segunda e quarta ordem: **RMS** (para medir a energia do sinal) e **Curtose** (para identificar picos gerados por falhas).
2. **Detecção de Novidades (Treinamento Isolado):** Para evitar o viés e o vazamento de dados (*data leakage*), a padronização de escala (`StandardScaler`) e o treinamento do modelo (`Isolation Forest`) foram realizados **exclusivamente com os dados do rolamento em estado saudável**.
3. **Filtro de Persistência Temporal:** Aplicação de uma regra de pós-processamento que exige a detecção de anomalias em três janelas consecutivas para acionar o alarme. Essa abordagem reduz drasticamente os falsos positivos causados por variações ou ruídos isolados.

---

## Resultados Finais

A arquitetura proposta resolveu com sucesso a limitação de densidade de anomalias comumente enfrentada pelo *Isolation Forest*. O modelo foi validado comparando o rolamento saudável (Baseline `97.mat`) com um rolamento com falha no anel interno (`105.mat`).

**Métricas de Desempenho alcançadas:**
* **Acurácia:** $99.72\%$
* **Precisão:** $100.00\%$ *(Zero alarmes falsos no estado normal)*
* **Recall:** $99.15\%$ *(Alta sensibilidade à falha)*
* **Latência Média de Inferência:** $\approx 22 \text{ms}$ por janela temporal.

Abaixo, o gráfico gerado pelo sistema demonstra o sinal de RMS em azul e os acionamentos de alarme do modelo demarcados em vermelho:

![Gráfico de Resultados](relatorios/grafico_final_pibic.png)

---

## Estrutura do Repositório

O repositório está estruturado seguindo boas práticas de engenharia de software para ciência de dados:

```text
├── data/                    # Base de dados original (os arquivos .mat do CWRU)
├── relatorios/              # Relatórios parciais/finais e saídas gráficas
├── src/               
│   ├── main.py              # Script organizador do fluxo de trabalho de Machine Learning
│   ├── processamento.py     # Funções para extração de dados e características
│   └── visualizacao.py      # Lógica para a plotagem dos gráficos (integração LaTeX/Matplotlib)
├── .gitignore         
├── README.md          
└── requirements.txt        # Lista de dependências do Python
```

---

## Como Executar

O projeto foi refatorado para execução direta e modularizada.

1. Clone este repositório:
   ```bash
   git clone https://github.com/Jhon-Victor-Ramos/pibic-deteccao-anomalias.git
   cd pibic-deteccao-anomalias
   ```
2. Crie um ambiente virtual (não é obrigatório, mas é recomendado) e instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o fluxo de trabalho principal:
   ```bash
   python src/main.py
   ```

---

## Autores

* **Jhon Victor Ramos Martins** - [GitHub](https://github.com/Jhon-Victor-Ramos) | [LinkedIn](https://www.linkedin.com/in/jhon-victor-ramos/)
* **Maria Luiza da Silva Monteiro** - [GitHub](https://github.com/Maria-Luiza-ds-Monteiro) | [LinkedIn](https://www.linkedin.com/in/maria-luiza-monteiro-6a7246280/)