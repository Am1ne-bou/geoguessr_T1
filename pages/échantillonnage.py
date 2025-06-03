import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Échantillonnage d'un Signal cosusoïdal",
    page_icon="📊",
    layout="wide")

st.title("Échantillonnage d'un Signal cosusoïdal")
st.write(
    """
    L'échantillonnage est le processus de conversion d'un signal continu en un signal discret en prenant des échantillons à intervalles réguliers.
    Dans cette application, nous allons visualiser comment l'échantillonnage affecte la représentation d'un signal cosusoïdal.
    """
)


col1, col2, col3, col4 = st.columns(4)

signals = []

with col1:
    st.header("Composante 1")
    A1 = st.number_input("Amplitude (A1)", min_value=0.0, value=1.0, step=0.1, key="A1")
    f1 = st.number_input("Fréquence (f1)", min_value=0.0, value=1.0, step=0.1, key="f1")
    phi1 = st.number_input("Phase (φ1)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f", key="phi1")
    signals.append({"A": A1, "f": f1, "phi": phi1})

with col2:
    st.header("Composante 2")
    A2 = st.number_input("Amplitude (A2)", min_value=0.0, value=0.8, step=0.1, key="A2")
    f2 = st.number_input("Fréquence (f2)", min_value=0.0, value=2.0, step=0.1, key="f2")
    phi2 = st.number_input("Phase (φ2)", min_value=0.0, max_value=float(2*np.pi), value=np.pi/2, step=0.1, format="%.2f", key="phi2")
    signals.append({"A": A2, "f": f2, "phi": phi2})

with col3:
    st.header("Composante 3")
    A3 = st.number_input("Amplitude (A3)", min_value=0.0, value=0.6, step=0.1, key="A3")
    f3 = st.number_input("Fréquence (f3)", min_value=0.0, value=3.0, step=0.1, key="f3")
    phi3 = st.number_input("Phase (φ3)", min_value=0.0, max_value=float(2*np.pi), value=np.pi, step=0.1, format="%.2f", key="phi3")
    signals.append({"A": A3, "f": f3, "phi": phi3})

with col4:
    st.header("Composante 4")
    A4 = st.number_input("Amplitude (A4)", min_value=0.0, value=0.4, step=0.1, key="A4")
    f4 = st.number_input("Fréquence (f4)", min_value=0.0, value=4.0, step=0.1, key="f4")
    phi4 = st.number_input("Phase (φ4)", min_value=0.0, max_value=float(2*np.pi), value=3*np.pi/2, step=0.1, format="%.2f", key="phi4")
    signals.append({"A": A4, "f": f4, "phi": phi4})


# Temps continu 
t = np.linspace(0, 1, 1000)

# Création du signal final en sommant les composantes
signal_final = np.zeros_like(t)
individual_signals = []

for sig in signals:
    component = sig["A"] * np.cos(2 * np.pi * sig["f"] * t + sig["phi"])
    signal_final += component
    individual_signals.append(component)

st.subheader("Formule du signal final")
st.latex(r"f(t) = " + " + ".join([f"A{i} \cos(2 \pi f{i} t + φ{i})" for i in range(1, 5)]))

st.subheader("visualisation des signaux ")

tab1, tab2= st.tabs(["Signal resultant", "Composantes Individuelles"])

with tab1:
    st.header("Signal Resultant")
    st.plotly_chart(go.Figure(data=go.Scatter(x=t, y=signal_final, mode='lines', name='Signal Resultant')))

with tab2:
    st.header("Composantes Individuelles")
    fig_individual = go.Figure()
    for i, component in enumerate(individual_signals, start=0):
        fig_individual.add_trace(go.Scatter(x=t, y=component, mode='lines', name=f'Composante {i+1}'))    
    st.plotly_chart(fig_individual)

# Fréquence d'échantillonnage
fs = st.slider("Fréquence d'échantillonnage (fs)",0, 1000, 100, step=10)

# Signal continu
y_continu = signal_final

# Temps échantillonné
t_sampled = np.arange(0, 1, 1/fs)

# Signal échantillonné
y_sampled = np.zeros_like(t_sampled)
for sig in signals:
    component_sampled = sig["A"] * np.cos(2 * np.pi * sig["f"] * t_sampled + sig["phi"])
    y_sampled += component_sampled

# Création du graphique avec Plotly
fig = go.Figure()

# Signal continue
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
    marker=dict(color='red', size=4)
))

# Mise en forme du graphique
fig.update_layout(
    title="Échantillonnage d'un Signal cosusoïdal",
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
peaks = (np.abs(amplitude) > 0.1)  # Seuil arbitraire

# Création du graphique pour le spectre de fréquence
fig_fft = go.Figure()
# Spectre
fig_fft.add_trace(go.Scatter(x=frequencies, y=np.zeros_like(frequencies),  
                         line=dict(color='white')))

# Marquage des pics
fig_fft.add_trace(go.Scatter(x=frequencies[peaks], y=amplitude[peaks],
                        mode='markers',
                        marker=dict(color='red', size=4)))

for freq, amp in zip(frequencies[peaks], amplitude[peaks]):
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
                 showlegend=False)


st.plotly_chart(fig_fft, use_container_width=True)



# Spectre de fréquence du signal échantillonné
fft_sampled = np.fft.fft(y_sampled)
frequencies_sampled = np.fft.fftfreq(len(y_sampled), 1/fs)[:len(y_sampled)//2]
amplitude_sampled = 2/len(y_sampled) * np.abs(fft_sampled[0:len(y_sampled)//2])
print(len(y_sampled), len(frequencies_sampled), len(amplitude_sampled))

repeat_factor = 5
frequencies_sampled_fin = np.tile(frequencies_sampled, repeat_factor) + np.repeat(np.arange(repeat_factor) * fs, len(frequencies_sampled))

amplitude_sampled_fin = np.zeros_like(frequencies_sampled_fin)
for i in range(0, repeat_factor):
    amplitude_sampled_fin[i*len(amplitude_sampled):(i+1)*len(amplitude_sampled)] += amplitude_sampled


# Affichage du spectre de fréquence du signal échantillonné
st.subheader("Spectre de Fréquence du Signal Échantillonné")

# Détection des pics dans le spectre échantillonné
peaks_sampled = (np.abs(amplitude_sampled_fin) > 0.1)  # Seuil arbitraire

# Création du graphique pour le spectre de fréquence échantillonné
fig_fft_sampled = go.Figure()

# Spectre échantillonné
fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin, y=np.zeros_like(frequencies_sampled_fin),
                         line=dict(color='black')))

# Marquage des pics échantillonnés
fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin[peaks_sampled], y=amplitude_sampled_fin[peaks_sampled],
                        mode='markers', 
                        marker=dict(color='red', size=4)))
for freq, amp in zip(frequencies_sampled_fin[peaks_sampled], amplitude_sampled_fin[peaks_sampled]):
    fig_fft_sampled.add_shape(
        type="line",
        x0=freq, y0=0,  # Starts at x-axis
        x1=freq, y1=amp,  # Ends at peak amplitude
        line=dict(color="red", width=1.5),
        opacity=0.8
    )
    # Ajouter des annotations pour les pics
    fig_fft_sampled.add_annotation(
        x=freq,
        y=amp,
        text=f"{freq:.1f} Hz",
        showarrow=False,
        yshift=10,
        font=dict(size=10)
    )
# Mise en forme du graphique échantillonné
fig_fft_sampled.update_layout(title='Spectre du signal Échantillonné ',
                             xaxis_title='Fréquence (Hz)',
                             yaxis_title='Amplitude',
                             showlegend=False)
st.plotly_chart(fig_fft_sampled, use_container_width=True)
 