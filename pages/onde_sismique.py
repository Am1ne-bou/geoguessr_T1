import numpy as np
import plotly.graph_objects as go
import streamlit as st
import scipy as sp

# Configuration de la page
st.set_page_config(
    page_title="Onde sismique",
    layout="wide")

st.title("Onde sismique")
st.header("1. Visualisation d'une onde sismique")
st.write(
    """
    Une onde sismique est une perturbation qui se propage dans la Terre, généralement causée par un séisme.
    Dans cette application, nous visualisons une onde sismique captee par une station japonaise.
    """
)
data=sp.io.loadmat("recording1.mat")

signal_5 = data["list"][0][4][0]
signal_x = []
signal_y = []
signal_z = []

time=np.linspace(0, 120, 12000)

for i in range(12000):
    signal_x.append(signal_5[i][0])
    signal_y.append(signal_5[i][1])
    signal_z.append(signal_5[i][2])



# Création du graphique
fig = go.Figure()
fig.add_trace(go.Scatter(x=time, y=signal_x, mode='lines', name='Signal nord_sud (X)',line=dict(color='blue')))
fig.add_trace(go.Scatter(x=time, y=signal_y, mode='lines', name='Signal est_ouest (Y)',line=dict(color='red')))
fig.add_trace(go.Scatter(x=time, y=signal_z, mode='lines', name='Signal vertical (Z)',line=dict(color='lime')))

fig.update_layout(
    title="Onde sismique captée par une station japonaise",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

tab1, tab2, tab3 = st.tabs(["Signal nord_sud (X)", "Signal est_ouest (Y)", "Signal vertical (Z)"])
with tab1:
    st.subheader("Signal nord_sud (X)")
    fig_x = go.Figure()
    fig_x.add_trace(go.Scatter(x=time, y=signal_x, mode='lines', name='Signal nord_sud (X)',line=dict(color='blue')))  
    fig_x.update_layout(
        title="Signal nord_sud (X)",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig_x, use_container_width=True)

with tab2:
    st.subheader("Signal est_ouest (Y)")
    fig_y = go.Figure()
    fig_y.add_trace(go.Scatter(x=time, y=signal_y, mode='lines', name='Signal est_ouest (Y)',line=dict(color='red')))
    fig_y.update_layout(
        title="Signal est_ouest (Y)",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig_y, use_container_width=True)

with tab3:
    st.subheader("Signal vertical (Z)")
    fig_z = go.Figure()
    fig_z.add_trace(go.Scatter(x=time, y=signal_z, mode='lines', name='Signal vertical (Z)',line=dict(color='lime')))
    fig_z.update_layout(
        title="Signal vertical (Z)",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig_z, use_container_width=True)

