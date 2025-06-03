import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Atelier : Filtrage fréquentiel d'un signal")


st.header("1. Génération d'un signal composé de 3 fréquences")
st.write(
    """
    Choisissez trois fréquences différentes pour générer un signal composé de trois cosinus.
    Vous pourrez ensuite appliquer différents filtres pour isoler chaque composante fréquentielle.
    """
)

A1 = st.slider("Amplitude fréquence 1 (A₁)", 0.0, 100.0, 30.0, 1.0)
f1 = st.slider("Fréquence 1 (Hz)", 1.0, 5.0, 2.0, 0.1)
A2 = st.slider("Amplitude fréquence 2 (A₂)", 0.0, 100.0, 20.0, 1.0)
f2 = st.slider("Fréquence 2 (Hz)", 6.0, 12.0, 8.0, 0.1)
A3 = st.slider("Amplitude fréquence 3 (A₃)", 0.0, 100.0, 15.0, 1.0)
f3 = st.slider("Fréquence 3 (Hz)", 13.0, 20.0, 15.0, 0.1)

t = np.linspace(0, 2, 2000)
signal = (
    A1 * np.cos(2 * np.pi * f1 * t) +
    A2 * np.cos(2 * np.pi * f2 * t) +
    A3 * np.cos(2 * np.pi * f3 * t)
)

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=signal, mode='lines', name='Signal à 3 fréquences'))
fig.update_layout(
    title="Signal composé de 3 fréquences",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig, use_container_width=True)

st.header("2. Spectre du signal")
N = len(t)
frequences = np.fft.fftfreq(N, d=(t[1]-t[0]))
spectre = np.abs(np.fft.fft(signal)) * 2 / N
mask = frequences >= 0  # On ne garde que les fréquences positives

fig_spectre = go.Figure()
fig_spectre.add_trace(go.Scatter(
    x=frequences[mask],
    y=spectre[mask],
    mode='lines',
    line=dict(color='red')
))
fig_spectre.update_layout(
    title="Spectre du signal (FFT)",
    xaxis_title="Fréquence (Hz)",
    yaxis_title="Amplitude",
    template="plotly_white",
    xaxis=dict(range=[0, 25])
)
st.plotly_chart(fig_spectre, use_container_width=True)


st.header("3. Filtrage fréquentiel (filtre parfait)")

filtre_type = st.radio(
    "Choisissez un type de filtre à appliquer :",
    ("Passe-bas (garde la fréquence 1)", "Passe-bande (garde la fréquence 2)", "Passe-haut (garde la fréquence 3)")
)


fft_signal = np.fft.fft(signal)
frequences_pos = frequences

if filtre_type == "Passe-bas (garde la fréquence 1)":
    fc = f1 + (f2 - f1) / 2
    mask_filtre = np.abs(frequences_pos) <= fc
elif filtre_type == "Passe-bande (garde la fréquence 2)":
    f_low = f2 - (f2 - f1) / 2
    f_high = f2 + (f3 - f2) / 2
    mask_filtre = (np.abs(frequences_pos) >= f_low) & (np.abs(frequences_pos) <= f_high)
else:  # Passe-haut
    fc = f2 + (f3 - f2) / 2
    mask_filtre = np.abs(frequences_pos) >= fc

fft_filtre = np.zeros_like(fft_signal)
fft_filtre[mask_filtre] = fft_signal[mask_filtre]

signal_filtre = np.fft.ifft(fft_filtre).real

fig_filtre = go.Figure()
fig_filtre.add_trace(go.Scatter(x=t, y=signal, mode='lines', name='Signal original', opacity=0.4))
fig_filtre.add_trace(go.Scatter(x=t, y=signal_filtre, mode='lines', name='Signal filtré', line=dict(color='green')))
fig_filtre.update_layout(
    title="Signal après filtrage parfait",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig_filtre, use_container_width=True)

st.write(
    """
    👉 Selon le filtre choisi, seule la composante fréquentielle correspondante est conservée.
    Essayez de changer les fréquences et d'appliquer différents filtres pour observer leur effet !
    """
)
