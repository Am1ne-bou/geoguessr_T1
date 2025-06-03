import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.title("Échantillonnage d'un Signal Sinusoïdal")
st.write(
    """
    L'échantillonnage est le processus de conversion d'un signal continu en un signal discret en prenant des échantillons à intervalles réguliers.
    Dans cette application, nous allons visualiser comment l'échantillonnage affecte la représentation d'un signal sinusoïdal.
    """
)

# Paramètres du signal
A = st.number_input("Amplitude (A)", min_value=0.0, max_value=100000.0, value=1.0, step=10.0)
f = st.number_input("Fréquence (f)", min_value=0.0, max_value=1000.0, value=1.0, step=1.0)
phi = st.number_input("Phase (φ en radians)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f")

# Paramètres d'échantillonnage
fs = st.slider("Fréquence d'échantillonnage (fs)",0, 1000, 100, step=10)


# Temps continu 
t = np.linspace(0, 1, 1000)
# Signal continu
y_continu = A * np.cos(2 * np.pi * f * t + phi)

# Temps échantillonné
t_sampled = np.arange(0, 1, 1/fs)

# Signal échantillonné
y_sampled = A * np.cos(2 * np.pi * f * t_sampled + phi)

# Création du graphique avec Plotly
fig = go.Figure()

# Signal continu (ligne bleue)
fig.add_trace(go.Scatter(
    x=t,
    y=y_continu,
    mode='lines',
    name='Signal Continu',
    line=dict(color='blue')
))

# Signal échantillonné (points rouges)
fig.add_trace(go.Scatter(
    x=t_sampled,
    y=y_sampled,
    mode='markers',
    name='Signal Échantillonné',
    marker=dict(color='red', size=8)
))

# Mise en forme du graphique
fig.update_layout(
    title="Échantillonnage d'un Signal Sinusoïdal",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    legend_title="Légende",
    hovermode="x unified"
)

# Affichage du graphique interactif
st.plotly_chart(fig, use_container_width=True)


# Explication de l'échantillonnage
st.write(
    """
    L'échantillonnage consiste à prélever des valeurs du signal continu à des intervalles réguliers.
    La fréquence d'échantillonnage (fs) doit être au moins le double de la fréquence du signal (f) pour éviter qu'on ne puisse pas reconstruire le signal, conformément au théorème de Shannon.
    """
)

#spectre de fréquence du signal continu


# Nombre de points
N = 1000



# Calcul de la FFT
fft_result = np.fft.fft(y_continu)
frequencies = np.fft.fftfreq(N, 1/N)[:N//2]  # Partie positive
amplitude = 2/N * np.abs(fft_result[0:N//2])  # Spectre d'amplitude

# Affichage du spectre de fréquence
st.subheader("Spectre de Fréquence du Signal Continu")

# Détection des pics dans le spectre
peaks = (amplitude > 0.5)  # Seuil arbitraire

# Création du graphique pour le spectre de fréquence
fig_fft = go.Figure()
# Spectre
fig_fft.add_trace(go.Scatter(x=frequencies, y=amplitude, 
                        name='Spectre', line=dict(color='blue')))

# Marquage des pics
fig_fft.add_trace(go.Scatter(x=frequencies[peaks], y=amplitude[peaks],
                        mode='markers', name='Pics',
                        marker=dict(color='red', size=8)))

# Mise en forme
fig_fft.update_layout(title='Spectre avec détection de pics',
                 xaxis_title='Fréquence (Hz)',
                 yaxis_title='Amplitude')  


st.plotly_chart(fig_fft, use_container_width=True)



# Spectre de fréquence du signal échantillonné
fft_sampled = np.fft.fft(y_sampled)
frequencies_sampled = np.fft.fftfreq(len(y_sampled), 1/fs)[:len(y_sampled)//2]
amplitude_sampled = 2/len(y_sampled) * np.abs(fft_sampled[0:len(y_sampled)//2])

repeat_factor = 5
frequencies_sampled_fin = np.tile(frequencies_sampled, repeat_factor) + np.repeat(np.arange(repeat_factor) * fs, len(frequencies_sampled))
amplitude_sampled_fin = np.tile(amplitude_sampled, repeat_factor)


# Affichage du spectre de fréquence du signal échantillonné
st.subheader("Spectre de Fréquence du Signal Échantillonné")

# Détection des pics dans le spectre échantillonné
peaks_sampled = (amplitude_sampled_fin > 0.5)  # Seuil arbitraire

# Création du graphique pour le spectre de fréquence échantillonné
fig_fft_sampled = go.Figure()

# Spectre échantillonné
fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin, y=amplitude_sampled_fin,
                        name='Spectre Échantillonné', line=dict(color='blue')))

# Marquage des pics échantillonnés
fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin[peaks_sampled], y=amplitude_sampled_fin[peaks_sampled],
                        mode='markers', name='Pics Échantillonnés',
                        marker=dict(color='red', size=8)))

# Mise en forme du graphique échantillonné
fig_fft_sampled.update_layout(title='Spectre Échantillonné avec Détection de Pics',
                             xaxis_title='Fréquence (Hz)',
                             yaxis_title='Amplitude')
st.plotly_chart(fig_fft_sampled, use_container_width=True)
 