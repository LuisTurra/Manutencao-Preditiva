# 🛠️ Projeto de Manutenção Preditiva de Máquinas Industriais

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)](https://plotly.com/)
[![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Kaggle](https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=for-the-badge)](https://github.com/Wrathh)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://luisturra-manutencao-preditiva-streamlit-app-4ew73b.streamlit.app)

**Portfolio Project – Ciência de Dados / Machine Learning**

Este projeto implementa um sistema completo de **manutenção preditiva** usando o dataset público **AI4I 2020 Predictive Maintenance Dataset** (disponível no Kaggle). O objetivo é prever falhas em máquinas industriais antes que elas ocorram, reduzindo paradas não planejadas e custos de manutenção.

O destaque do projeto é o **dashboard interativo em Streamlit** que simula monitoramento em tempo real de 4 máquinas, com gauges circulares, alertas coloridos, parâmetros visíveis e histórico automático de falhas de alto risco.

[![Streamlit App] https://luisturra-manutencao-preditiva-streamlit-app-4ew73b.streamlit.app/ 

## 🎯 Objetivo de Negócio
- Prever **Machine failure** (falha da máquina) a partir de sensores (temperatura, torque, velocidade, desgaste etc.).
- Classes altamente desbalanceadas (~3% falhas) → foco em **ROC AUC** (discriminação geral) e **Recall** (detectar o máximo de falhas reais).
- Impacto real: manutenção preventiva pode reduzir downtime em até 70–80% em indústrias manufatureiras.

## 📊 Dataset
- **Fonte**: [AI4I 2020 Predictive Maintenance Dataset](https://www.kaggle.com/datasets/stephanmatzka/predictive-maintenance-dataset-ai4i-2020)
- ~10.000 registros sintéticos, mas realistas, de uma linha de produção.
- Features principais:
  - Type (L/M/H) – tipo de produto
  - Air temperature [K]
  - Process temperature [K]
  - Rotational speed [rpm]
  - Torque [Nm]
  - Tool wear [min]
- Target: Machine failure (binário)

## 🔬 Abordagem Técnica

### 1. Exploração (EDA) – `notebooks/01_eda.ipynb`
- Análise de distribuições, correlações e padrões de falha.
- Visualizações: histograms, boxplots, heatmap de correlação, contagens por tipo.

### 2. Modelagem – `notebooks/02_model_training.ipynb`
- Pré-processamento: drop de colunas inúteis, encoding de `Type`.
- Comparação rigorosa de 4 modelos usando **Stratified 5-fold Cross-Validation** + hold-out test.
- Métricas priorizadas: **ROC AUC** e **Recall** (devido ao desbalanceamento).

#### Resultados da Comparação de Modelos

| Modelo                | AUC CV Mean | AUC CV Std | Recall CV Mean | AUC Test | Recall Test |
|-----------------------|-------------|------------|----------------|----------|-------------|
| Gradient Boosting     | **0.9728**  | 0.0120     | 0.6681         | **0.9698**| 0.7059      |
| Random Forest         | 0.9711      | 0.0131     | 0.6128         | 0.9611   | 0.7206      |
| Extra Trees           | 0.9558      | 0.0082     | 0.7601         | 0.9593   | 0.7941      |
| Logistic Regression   | 0.8956      | 0.0162     | **0.8156**     | 0.9065   | **0.8235**  |

**Análise dos resultados**:
- **Gradient Boosting** obteve o **melhor AUC** (≈0.97 no teste), indicando excelente capacidade de discriminação geral.
- Modelos baseados em árvores (Gradient Boosting, Random Forest, Extra Trees) superam amplamente a regressão logística em AUC.
- **Logistic Regression** e **Extra Trees** têm maior Recall, mas com custo de mais falsos positivos (menor AUC).
- O modelo selecionado automaticamente (`best_model.pkl`) foi o **Gradient Boosting**, priorizando AUC alto com Recall razoável – equilíbrio ideal para manutenção preditiva (evitar tanto falhas perdidas quanto manutenções desnecessárias).

### 3. Dashboard – `app.py`
- **Aba 1 – Monitoramento Automático**:
  - Simula 4 máquinas com dados gerados aleatoriamente (distribuições idênticas ao dataset real).
  - Atualização automática a cada 10 segundos.
  - Gauges circulares (Plotly) com probabilidade de falha.
  - Status colorido: Verde (<10%), Amarelo (10–50%), Vermelho (>50%).
  - Parâmetros atuais exibidos como métricas.
- **Aba 2 – Entrada Manual**: teste livre com sliders.

## 🚀 Como Executar Localmente

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/predictive-maintenance-portfolio.git
   cd predictive-maintenance-portfolio

2. Crie e ative um ambiente virtual (recomendado):bash
    ```bash
    python -m venv venv
    source venv/bin/activate  
    venv\Scripts\activate     

3. Instale as dependências:bash
    ```bash
    pip install -r requirements.txt

4. Rode os notebooks para gerar o modelo (se necessário):Abra notebooks/02_model_training.ipynb  e execute todas as células.

5. Inicie o dashboard:bash
    ```bash
    streamlit run app.py

## Deploy ## 
Deploy gratuito no Streamlit Community Cloud.


 ### Tecnologias Utilizadas
Python, Pandas, Scikit-learn, XGBoost/GradientBoosting
Matplotlib, Seaborn, Plotly
Streamlit + streamlit-autorefresh
Joblib para salvar modelo

## Por que este projeto?
Pipeline completo: EDA → modelagem comparativa → deploy interativo.
Foco em impacto de negócio (manutenção preditiva).
Dashboard realista e visualmente atraente (gauges, auto-refresh, histórico).
Boas práticas: separação de concerns, código limpo, persistência com session_state.

Qualquer dúvida ou sugestão, entre em contato! 
Feito por Luis Henrique Turra Ramos – 2026
