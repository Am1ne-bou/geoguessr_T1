import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Visualisation interactive d'un signal sinusoïdal")
st.header("1. Visualisation du signal $A \\cos(2\\pi f t + \\phi)$")
st.write(
    """
    Un signal est une grandeur physique qui varie en fonction du temps et qui peut transporter de l'information.
    Dans cette application, on visualise un signal sinusoïdal de la forme $A \\cos(2\\pi f t + \\phi)$, où :
    - $A$ est l'amplitude,
    - $f$ la fréquence,
    - $\\phi$ la phase.
    Vous pouvez modifier ces paramètres pour observer leur influence sur la forme du signal.
    """
)
A = st.slider("Amplitude (A)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
f = st.slider("Fréquence (f)", min_value=4.0, max_value=15.0, value=1.0, step=0.1)
phi = st.slider("Phase (φ en radians)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f")

t = np.linspace(0, 2, 1000)
y = A * np.cos(2 * np.pi * f * t + phi)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, mode='lines',
                         name=fr'$A={A},\ f={f},\ \phi={phi:.2f}$'))
fig.update_layout(
    title={
        'text': "<span style='font-size:20px;'>A&nbsp;cos(2πft&nbsp;+&nbsp;φ)</span>",
        'x': 0.5
    },
    xaxis_title='Temps (t)',
    yaxis_title='Amplitude',
    legend_title='Paramètres',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

st.header("2. Spectre du signal (analyse des fréquences)")
st.write(
    """
    **Le spectre** montre quelles fréquences composent le signal.  
    Pour un son pur comme celui-ci représenté par un cosinus, on voit un seul pic à la fréquence du signal !
    """
)
st.write(
    """
    Un signal peut s'analyser de deux façons :
    - **Dans le temps** : on voit comment il évolue seconde après seconde
    - **En fréquence** : on voit quelles fréquences le composent
    
    Essayez de modifier les paramètres pour voir comment le spectre change !
    """
)
N = len(t)
frequences = np.fft.fftfreq(N, d=(t[1]-t[0]))[:N//2]  
spectre = np.abs(np.fft.fft(y))[:N//2] * 2/N 

fig_spectre = go.Figure()
fig_spectre.add_trace(go.Scatter(
    x=frequences,
    y=spectre,
    mode='lines',
    line=dict(color='red')
))
fig_spectre.update_layout(
    title="Spectre du signal",
    xaxis_title='Fréquence (Hz)',
    yaxis_title='Amplitude',
    template='plotly_white',
    showlegend=False,
    xaxis=dict(range=[0, 20]),
)

st.plotly_chart(fig_spectre, use_container_width=True)