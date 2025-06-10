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
    f1 = st.number_input("Fréquence (f1)", min_value=0.0, value=10.0, step=0.1, key="f1")
    phi1 = st.number_input("Phase (φ1)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f", key="phi1")
    signals.append({"A": A1, "f": f1, "phi": phi1})

with col2:
    st.header("Composante 2")
    A2 = st.number_input("Amplitude (A2)", min_value=0.0, value=0.8, step=0.1, key="A2")
    f2 = st.number_input("Fréquence (f2)", min_value=0.0, value=30.0, step=0.1, key="f2")
    phi2 = st.number_input("Phase (φ2)", min_value=0.0, max_value=float(2*np.pi), value=np.pi/2, step=0.1, format="%.2f", key="phi2")
    signals.append({"A": A2, "f": f2, "phi": phi2})

with col3:
    st.header("Composante 3")
    A3 = st.number_input("Amplitude (A3)", min_value=0.0, value=0.6, step=0.1, key="A3")
    f3 = st.number_input("Fréquence (f3)", min_value=0.0, value=50.0, step=0.1, key="f3")
    phi3 = st.number_input("Phase (φ3)", min_value=0.0, max_value=float(2*np.pi), value=np.pi, step=0.1, format="%.2f", key="phi3")
    signals.append({"A": A3, "f": f3, "phi": phi3})

with col4:
    st.header("Composante 4")
    A4 = st.number_input("Amplitude (A4)", min_value=0.0, value=0.4, step=0.1, key="A4")
    f4 = st.number_input("Fréquence (f4)", min_value=0.0, value=70.0, step=0.1, key="f4")
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
fs = st.slider("Fréquence d'échantillonnage (fs)",0, 1000, 200, step=10, key="fs")

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
# Mettre en evidence la frequence d'échantillonnage
fig_fft.add_vline(
    x=fs,
    line=dict(color='green', dash='dash'),
    annotation_text="fs",
    annotation_position="top right"
)
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
                 xaxis_range=[0, fs*1.05],
                 showlegend=False)


st.plotly_chart(fig_fft, use_container_width=True)


fc = st.slider("Fréquence de coupure (fc)",0, 500, 50, step=5, key="fc")

# Spectre de fréquence du signal échantillonné
fft_sampled = np.fft.fft(y_sampled)
frequencies_sampled = np.fft.fftfreq(len(y_sampled), 1/fs)
amplitude_sampled = 2/len(y_sampled) * np.abs(fft_sampled)




frequencies_half = frequencies_sampled[0:len(y_sampled)//2]
frequencies_sampled_fin = np.tile(frequencies_half, 2) + np.repeat([0, fs/2], len(frequencies_half))

amplitude_sampled_fin = np.zeros_like(frequencies_sampled_fin)
half_y_sampled = len(y_sampled) // 2
amplitude_sampled_fin[0:half_y_sampled] = amplitude_sampled[0:half_y_sampled]
amplitude_sampled_fin[half_y_sampled:] = amplitude_sampled[-half_y_sampled:]


# Affichage du spectre de fréquence du signal échantillonné
st.subheader("Spectre de Fréquence du Signal Échantillonné")

# Détection des pics dans le spectre échantillonné
peaks_sampled = (np.abs(amplitude_sampled_fin) > 0.1)  # Seuil arbitraire

# Création du graphique pour le spectre de fréquence échantillonné
fig_fft_sampled = go.Figure()



# Spectre échantillonné
# Mettre en evidence la frequence d'échantillonnage
fig_fft_sampled.add_vline(
    x=fs,
    line=dict(color='green', dash='dash', width=2),
    annotation_text="fs",
    annotation_position="top right"
)
fig_fft_sampled.add_vline(
    x=fc,
    line=dict(color='blue', dash='dash', width=2),
    annotation_text="fc",
    annotation_position="top right"
    )

fig_fft_sampled.add_vline(
    x=fs/2,
    line=dict(color='orange', dash='solid' , width=2),
    annotation_text="fs/2",
    annotation_position="top right"
    )

fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin, y=np.zeros_like(frequencies_sampled_fin),
                         line=dict(color='black')))

# Marquage des pics échantillonnés
fig_fft_sampled.add_trace(go.Scatter(x=frequencies_sampled_fin[peaks_sampled], y=amplitude_sampled_fin[peaks_sampled],
                        mode='markers', 
                        marker=dict(color='red', size=4)))
for freq, amp in zip(frequencies_sampled_fin[peaks_sampled], amplitude_sampled_fin[peaks_sampled]):
    fig_fft_sampled.add_shape(
        type="line",
        x0=freq, y0=0,  
        x1=freq, y1=amp,  
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
                             xaxis_range=[0, fs*1.05],
                             showlegend=False)


st.plotly_chart(fig_fft_sampled, use_container_width=True)

#le bonne foix de la fréquence de coupure pour avoir un signal reconstruit fidèle



prob_fc = False
y_fc= np.zeros_like(t)

num_peak = 0
# Compter le nombre de pics dans le spectre échantillonné
for freq, amp in zip(frequencies_sampled_fin, amplitude_sampled_fin):
    if amp > 0.1:  # Seuil arbitraire pour éviter les petites amplitudes
        if freq <= fc :  
            num_peak+=1

phase=[sig["phi"] for sig in signals]
if num_peak-4 > 0:
    phase += [0 for i in range(num_peak-4)]
if num_peak <= 4:
    phase = phase[:num_peak]

indice_phase = 0
while indice_phase < len(phase):
    for freq, amp in zip(frequencies_sampled_fin, amplitude_sampled_fin):
        if amp > 0.1:  # Seuil arbitraire pour éviter les petites amplitudes
            if freq <= fc :  
                y_fc+= amp * np.cos(2 * np.pi * freq * t + phase[indice_phase])
                indice_phase += 1

if np.allclose(y_fc, y_continu):
    prob_fc = False
else:
    prob_fc = True






fig_fc = go.Figure()

fig_fc.add_trace(go.Scatter(
    x=t,
    y=y_continu,
    mode='lines',
    name='Signal Continu',
    line=dict(color='blue')
))
fig_fc.add_trace(go.Scatter(
    x=t,
    y=y_fc,
    mode='lines',   
    name='Signal Reconstruit',
    line=dict(color='orange')
    ))

fig_fc.update_layout(
    title="Signal Reconstruit à partir du Spectre Échantillonné",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    legend_title="Légende",
    hovermode="x unified"
)



prob_construction = False
y_reconstructed = np.zeros_like(t)

num_peak = 0
# Compter le nombre de pics dans le spectre échantillonné
for freq, amp in zip(frequencies_sampled_fin, amplitude_sampled_fin):
    if amp > 0.1:  # Seuil arbitraire pour éviter les petites amplitudes
        if freq <= fs / 2:  # Vérification de la condition de Nyquist
            num_peak+=1

phase=[sig["phi"] for sig in signals]
if num_peak-4 > 0:
    phase += [0 for i in range(num_peak-4)]
if num_peak <= 4:
    phase = phase[:num_peak]

indice_phase = 0
while indice_phase < len(phase):
    for freq, amp in zip(frequencies_sampled_fin, amplitude_sampled_fin):
        if amp > 0.1:  # Seuil arbitraire pour éviter les petites amplitudes
            if freq <= fs / 2:  # Vérification de la condition de Nyquist
                y_reconstructed += amp * np.cos(2 * np.pi * freq * t + phase[indice_phase])
                indice_phase += 1

if np.allclose(y_reconstructed, y_continu):
    prob_construction = False
else:
    prob_construction = True






fig_reconstructed = go.Figure()

fig_reconstructed.add_trace(go.Scatter(
    x=t,
    y=y_continu,
    mode='lines',
    name='Signal Continu',
    line=dict(color='blue')
))
fig_reconstructed.add_trace(go.Scatter(
    x=t, 
    y=y_reconstructed, 
    mode='lines', 
    name='Signal Reconstruit',
    line=dict(color='orange')
    ))

fig_reconstructed.update_layout(
    title="Signal Reconstruit à partir du Spectre Échantillonné",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    legend_title="Légende",
    hovermode="x unified"
)




tab3, tab4 = st.tabs(["1", "2"])
with tab3:
    #Affichage du signal reconstruit
    st.subheader("Signal Reconstruit à partir du Spectre Échantillonné")


    st.write(""" on change la fréquence de coupure fc pour voir son impact sur la reconstruction du signal échantillonné.""")

    st.plotly_chart(fig_fc, use_container_width=True, key="reconstructed_chart_fc")

    if prob_fc:
        st.warning("Le signal reconstruit n'est pas fidèle au signal original car fc utiliser n'est pas adéquate." \
        "Si fc est trop bas, certaines fréquences du signal original seront perdues, ce qui peut entraîner une perte d'information dans le signal reconstruit. " \
        "Si fc est trop élevé, cela peut également entraîner une perte d'information car on ajoute des fréquences qui n'étaient pas présentes dans le signal original.")
    else:
        st.success("Le signal reconstruit est fidèle au signal original car seulement les fréquences de signal original qui sont présentes dans la partie de spectre qu'on utilise pour la reconstruction. "
                "Cela permet une reconstruction précise du signal échantillonné.")


with tab4:

    st.subheader("Reconstruction du Signal à partir du Spectre Échantillonné")

    st.write("""On change la fréquence d'échantillonnage fs pour voir son impact sur la reconstruction du signal échantillonné.""")

    st.write("""Le repliement spectral est un phénomène qui se produit lorsque la fréquence d'échantillonnage n'est pas suffisante pour capturer les variations du signal original.
    Cela peut entraîner une distorsion du signal reconstruit, car les hautes fréquences du signal original sont mal représentées ou perdues.""")

    st.write("""
    Selon le théorème de Nyquist-Shannon, pour éviter tout repliement spectral, la fréquence d'échantillonnage doit être au moins deux fois supérieure à la fréquence maximale du signal.
    Ce test vous permet de voir si la condition de Nyquist est respectée et si elle suffit à reconstruire correctement le signal.
    """)

    st.plotly_chart(fig_reconstructed, use_container_width=True, key="reconstructed_chart_fs")

    if prob_construction:
        st.warning("Le signal reconstruit n'est pas fidèle car la condition de Nyquist n'est pas respectée : certaines composantes fréquentielles sont perdues ou mal représentées.")
    else:
        st.success("La reconstruction du signal est correcte car la condition de Nyquist est respectée : fs ≥ 2 * f_max. Toutes les composantes du signal ont été bien échantillonnées et reconstituées.")
