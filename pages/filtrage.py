import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Introduction au filtrage d'un signal")

# --- 1. Génération du signal bruité ---
st.header("1. Génération d'un signal sinusoïdal bruité")
st.write(
    """
    On commence par générer un signal sinusoïdal auquel on ajoute du bruit aléatoire.
    Cela simule un signal réel mesuré, souvent perturbé par des parasites.
    """
)
A = st.slider("Amplitude du signal (A)", 0.0, 100.0, 20.0, 1.0)
f = st.slider("Fréquence du signal (f)", 1.0, 10.0, 2.0, 0.1)
phi = st.slider("Phase (φ en radians)", 0.0, float(2*np.pi), 0.0, 0.1, format="%.2f")
bruit = st.slider("Amplitude du bruit", 0.0, 50.0, 10.0, 1.0)

t = np.linspace(0, 2, 1000)
signal_pur = A * np.cos(2 * np.pi * f * t + phi)
np.random.seed(42)
bruit_alea = bruit * np.random.randn(len(t))
signal_bruite = signal_pur + bruit_alea

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=t, y=signal_pur, mode='lines', name='Signal pur'))
fig1.add_trace(go.Scatter(x=t, y=signal_bruite, mode='lines', name='Signal bruité', opacity=0.7))
fig1.update_layout(
    title="Signal pur et signal bruité",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig1, use_container_width=True)

# --- 2. Filtrage du signal ---
st.header("2. Filtrage du signal bruité (filtre passe-bas simple)")
st.write(
    """
    On applique un filtre passe-bas pour atténuer le bruit.
    Ce filtre remplace chaque valeur par la moyenne de ses voisines.
    """
)
N = st.slider("Taille de la fenêtre de filtrage (nombre de points)", 1, 101, 21, 2)
if N % 2 == 0:
    N += 1

def filtre_moyenne_glissante(signal, N):
    return np.convolve(signal, np.ones(N)/N, mode='same')
signal_filtre = filtre_moyenne_glissante(signal_bruite, N)

fig2 = go.Figure()
fig2.add_trace(go.Scatter(x=t, y=signal_bruite, mode='lines', name='Signal bruité', opacity=0.5))
fig2.add_trace(go.Scatter(x=t, y=signal_filtre, mode='lines', name='Signal filtré', line=dict(color='red')))
fig2.update_layout(
    title="Effet du filtrage sur le signal bruité",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig2, use_container_width=True)

st.write(
    """
    👉 On voit que le filtre permet de retrouver la forme générale du signal en atténuant le bruit !
    Essayez de modifier l'amplitude du bruit ou la taille de la fenêtre de filtrage pour voir l'effet.
    """
)
