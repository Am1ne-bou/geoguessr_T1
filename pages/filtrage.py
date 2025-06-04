import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Atelier : Filtrage fréquentiel d'un signal")

st.header("1. Génération d'un signal composé de 9 fréquences")
st.write(
    """
    Entrez 9 fréquences différentes pour générer un signal composé de 9 cosinus (amplitude 1 pour chaque).
    Vous pourrez ensuite appliquer un filtre parfait pour isoler une composante.
    """
)

frequences = []
for i in range(1, 10):
    freq = st.number_input(f"Fréquence f{i} (Hz)", min_value=1.0, max_value=50.0, value=float(2*i), step=0.1, key=f"freq_{i}")
    frequences.append(freq)
amplitudes = [1.0] * 9

t = np.linspace(0, 2, 4000)
signal = np.zeros_like(t)
for A, f in zip(amplitudes, frequences):
    signal += A * np.cos(2 * np.pi * f * t)
# Affichage du signal dans le temps
st.subheader("Signal dans le temps")
fig_filtre = go.Figure()
fig_filtre.add_trace(go.Scatter(x=t, y=signal, mode='lines', name='Signal original'))

fig_filtre.update_layout(
    title="Signal ",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
st.plotly_chart(fig_filtre, use_container_width=True)

st.header("2. Spectre du signal")
N = len(t)
freqs_fft = np.fft.fftfreq(N, d=(t[1]-t[0]))
spectre = np.abs(np.fft.fft(signal)) * 2 / N
mask = freqs_fft >= 0

peaks_fft = (np.abs(spectre) > 0.1)  # Seuil arbitraire

fig_fft = go.Figure()
fig_fft.add_trace(go.Scatter(x=freqs_fft, y=np.zeros_like(freqs_fft),  
                         line=dict(color='white')))

# Marquage des pics
fig_fft.add_trace(go.Scatter(x=freqs_fft[peaks_fft], y=spectre[peaks_fft],
                        mode='markers',
                        marker=dict(color='red', size=4)))

for freq, amp in zip(freqs_fft[peaks_fft], spectre[peaks_fft]):
    fig_fft.add_shape(
        type="line",
        x0=freq, y0=0,  # Starts at x-axis
        x1=freq, y1=amp,  # Ends at peak amplitude
        line=dict(color="red", width=1.5),
        opacity=0.8
    )
    # Ajouter des annotations pour les pics
    fig_fft.add_annotation(
        x=freq,
        y=amp,
        text=f"{freq:.1f} Hz",
        showarrow=False,
        yshift=10,
        font=dict(size=10)
    )

# Mise en forme
fig_fft.update_layout(title='Spectre ',
                 xaxis_title='Fréquence (Hz)',
                 yaxis_title='Amplitude',
                 xaxis_range=[0, max(frequences)*1.05],
                 showlegend=False)

st.plotly_chart(fig_fft, use_container_width=True)

st.header("3. Filtrage fréquentiel (filtre parfait)")

filtre_type = st.radio(
    "Choisissez un type de filtre à appliquer :",
    ("Passe-bas", "Passe-bande", "Passe-haut")
)

if filtre_type == "Passe-bas":
    fc = st.slider("Fréquence de coupure (Hz)", min_value=min(frequences), max_value=max(frequences), value=min(frequences), step=0.1)
    mask_filtre = np.abs(freqs_fft) <= fc
elif filtre_type == "Passe-haut":
    fc = st.slider("Fréquence de coupure (Hz)", min_value=min(frequences), max_value=max(frequences), value=max(frequences), step=0.1)
    mask_filtre = np.abs(freqs_fft) >= fc
else:  # Passe-bande
    f_low = st.slider("Borne basse (Hz)", min_value=min(frequences), max_value=max(frequences)-0.1, value=min(frequences), step=0.1)
    f_high = st.slider("Borne haute (Hz)", min_value=f_low+0.1, max_value=max(frequences), value=max(frequences), step=0.1)
    mask_filtre = (np.abs(freqs_fft) >= f_low) & (np.abs(freqs_fft) <= f_high)

fft_signal = np.fft.fft(signal)
fft_filtre = np.zeros_like(fft_signal)
fft_filtre[mask_filtre] = fft_signal[mask_filtre]
signal_filtre = np.fft.ifft(fft_filtre).real

# Spectre du signal filtré
spectre_filtre = np.abs(fft_filtre) * 2 / N
# Détection des pics dans le spectre
peaks = (np.abs(spectre_filtre) > 0.1)  

st.subheader("Spectre du signal filtré")
fig_fft_filtre = go.Figure()
# Mettre en évidence la fréquence de coupure
if filtre_type == "Passe-bas"or filtre_type == "Passe-haut":
    fig_fft_filtre.add_vline(
        x=fc,
        line=dict(color='green', dash='dash'),
        annotation_text="fc",
        annotation_position="top right"
    )
elif filtre_type == "Passe-bande":
    fig_fft_filtre.add_vline(
        x=f_low,
        line=dict(color='green', dash='dash'),
        annotation_text="f_low",
        annotation_position="top right"
    )
    fig_fft_filtre.add_vline(
        x=f_high,
        line=dict(color='green', dash='dash'),
        annotation_text="f_high",
        annotation_position="top right"
    )


fig_fft_filtre.add_trace(go.Scatter(x=freqs_fft, y=np.zeros_like(freqs_fft),  
                         line=dict(color='white')))

# Marquage des pics
fig_fft_filtre.add_trace(go.Scatter(x=freqs_fft[peaks], y=spectre_filtre[peaks],
                        mode='markers',
                        marker=dict(color='red', size=4)))

for freq, amp in zip(freqs_fft[peaks], spectre_filtre[peaks]):
    fig_fft_filtre.add_shape(
        type="line",
        x0=freq, y0=0,  # Starts at x-axis
        x1=freq, y1=amp,  # Ends at peak amplitude
        line=dict(color="red", width=1.5),
        opacity=0.8
    )
    fig_fft_filtre.add_annotation(
        x=freq,
        y=amp,
        text=f"{freq:.1f} Hz",
        showarrow=False,
        yshift=10,
        font=dict(size=10)
    )

# Mise en forme
fig_fft_filtre.update_layout(title='Spectre ',
                 xaxis_title='Fréquence (Hz)',
                 yaxis_title='Amplitude',
                 xaxis_range=[0, max(frequences)*1.05],
                 showlegend=False)

st.plotly_chart(fig_fft_filtre, use_container_width=True)

# Affichage du signal filtré
st.subheader("Signal dans le temps après filtrage")
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
    👉 Modifiez les paramètres du filtre pour isoler une seule fréquence parmi les 9 composantes du signal.
    Observez le spectre du signal filtré pour voir le pic de fréquence correspondant !
    """
)
