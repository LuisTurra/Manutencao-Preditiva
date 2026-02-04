
import streamlit as st
import joblib
import numpy as np
import plotly.graph_objects as go
import os
from streamlit_autorefresh import st_autorefresh

# Carrega o melhor modelo
model_path = 'C:/Users/Microsoft/Desktop/Projects/Python Projects/Manutencao-Preditiva/notebooks/model/best_model.pkl'

if not os.path.exists(model_path):
    st.error("🚨 Modelo não encontrado! Rode o notebook de treinamento para gerar 'best_model.pkl'.")
    st.stop()

model = joblib.load(model_path)

# Mapeamento LabelEncoder
type_mapping = {'H': 0, 'L': 1, 'M': 2}

# Stats reais do dataset 
type_choices = ['H', 'L', 'M']
type_probs = [0.1005, 0.5998, 0.2997] 

means = {'Air': 300.00493, 'Process': 310.00548, 'Rot': 1538.77624, 'Torque': 39.98717, 'Wear': 107.951}
stds  = {'Air': 2.00033, 'Process': 1.48381, 'Rot': 179.284, 'Torque': 9.96831, 'Wear': 63.31268}

mins = {'Air': 295.3, 'Process': 305.7, 'Rot': 1168, 'Torque': 3.8, 'Wear': 0}
maxs = {'Air': 304.5, 'Process': 313.8, 'Rot': 2886, 'Torque': 76.6, 'Wear': 253}

def generate_machine_data():
    type_str = np.random.choice(type_choices, p=type_probs)
    type_enc = type_mapping[type_str]
    
    air = np.clip(np.random.normal(means['Air'], stds['Air']), mins['Air'], maxs['Air'])
    process = np.clip(np.random.normal(means['Process'], stds['Process']), mins['Process'], maxs['Process'])
    rot = np.clip(np.random.normal(means['Rot'], stds['Rot']), mins['Rot'], maxs['Rot'])
    torque = np.clip(np.random.normal(means['Torque'], stds['Torque']), mins['Torque'], maxs['Torque'])
    wear = np.clip(np.random.normal(means['Wear'], stds['Wear']), mins['Wear'], maxs['Wear'])
    
    return {
        'Type': type_str,
        'Air temperature [K]': round(air, 1),
        'Process temperature [K]': round(process, 1),
        'Rotational speed [rpm]': int(rot),
        'Torque [Nm]': round(torque, 1),
        'Tool wear [min]': int(wear),
        'values': [type_enc, air, process, rot, torque, wear]
    }

def create_gauge(prob_percentage, machine_name):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob_percentage,
        number={'suffix': "%", 'font': {'size': 40}},
        title={'text': f"{machine_name}<br>Probabilidade de Falha", 'font': {'size': 18}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1},
            'bar': {'color': "black"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 10], 'color': '#90EE90'},   
                {'range': [10, 50], 'color': '#FFFF99'},  
                {'range': [50, 100], 'color': '#FFB6C1'}  
            ],
            'threshold': {
                'line': {'color': "red", 'width': 6},
                'thickness': 0.75,
                'value': 50
            }
        }
    ))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=80, b=20))
    return fig

# Interface principal
st.set_page_config(page_title="Manutenção Preditiva", layout="wide")
st.title("🛠️ Dashboard de Manutenção Preditiva – 4 Máquinas")

tabs = st.tabs(["📊 Monitoramento Automático", "🖐️ Entrada Manual"])

with tabs[0]:
    st.header("Monitoramento em Tempo Real (atualiza automaticamente a cada 10s)")
    
    # Auto-refresh a cada 10 segundos
    st_autorefresh(interval=10_000, key="auto_refresh_machines")
    
    # Gera novas leituras a cada refresh
    machines = [generate_machine_data() for _ in range(4)]
    
    cols = st.columns(4)
    for i, machine in enumerate(machines):
        with cols[i]:
            st.subheader(f"**Máquina {i+1}** – Tipo {machine['Type']}")
            
            # Previsão
            input_data = np.array([machine['values']])
            prob = model.predict_proba(input_data)[0][1]
            prob_pct = prob * 100
            
            # Gauge circular
            st.plotly_chart(create_gauge(prob_pct, f"Máquina {i+1}"), use_container_width=True)
            
            # Status textual com cor
            if prob > 0.5:
                st.error("🚨 **ALTO RISCO** – Manutenção imediata!")
            elif prob > 0.1:
                st.warning("⚠️ **RISCO MODERADO** – Monitorar")
            else:
                st.success("✅ **BAIXO RISCO** – Normal")
            
            # Parâmetros 
            st.markdown("**Parâmetros atuais:**")
            col1, col2 = st.columns(2)
            col1.metric("Temperatura do Ar [K]", machine['Air temperature [K]'])
            col2.metric("Temperatura do Processo [K]", machine['Process temperature [K]'])
            col1.metric("Velocidade Rotacional [rpm]", machine['Rotational speed [rpm]'])
            col2.metric("Torque [Nm]", machine['Torque [Nm]'])
            col1.metric("Desgaste da Ferramenta [min]", machine['Tool wear [min]'])

with tabs[1]:
    st.header("Entrada Manual – Teste um caso específico")
    
    type_options = {'H': 0, 'L': 1, 'M': 2}
    product_type = st.selectbox("Tipo de Produto", options=['H', 'L', 'M'])
    
    air_temp = st.slider("Air temperature [K]", 295.0, 305.0, 300.0, 0.1)
    process_temp = st.slider("Process temperature [K]", 305.0, 315.0, 310.0, 0.1)
    rot_speed = st.slider("Rotational speed [rpm]", 1100, 2900, 1500, 10)
    torque = st.slider("Torque [Nm]", 3.0, 80.0, 40.0, 0.5)
    tool_wear = st.slider("Tool wear [min]", 0, 250, 100, 1)
    
    input_data = np.array([[type_options[product_type], air_temp, process_temp, rot_speed, torque, tool_wear]])
    
    prob = model.predict_proba(input_data)[0][1]
    prob_pct = prob * 100
    
    st.plotly_chart(create_gauge(prob_pct, "Caso Manual"), use_container_width=True)
    
    if prob > 0.5:
        st.error("🚨 ALTO RISCO DE FALHA")
    elif prob > 0.1:
        st.warning("⚠️ RISCO MODERADO")
    else:
        st.success("✅ Baixo risco")

st.caption("Dashboard desenvolvido com Streamlit + Plotly. Modelo treinado com comparação de múltiplos algoritmos.")