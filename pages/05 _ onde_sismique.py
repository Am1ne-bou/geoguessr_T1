import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots 
import streamlit as st
import scipy as sp


# Configuration de la page
st.set_page_config(
    page_title="Onde sismique",
    layout="wide")

st.title("Onde sismique")


# Introduction
st.subheader("Introduction")
st.write(
    """
    Cette application permet de visualiser et d'écouter une onde sismique .
    Elle permet également de détecter les ondes P et S dans les signaux sismiques.
    Pour but de estimer la distance à l'épicentre du séisme.
    Vous pouvez interagir avec les graphiques et les paramètres pour mieux comprendre le comportement des ondes sismiques.
    """
)


st.header("1. Visualisation d'une onde sismique")
st.write(
    """
    Une onde sismique est une perturbation qui se propage dans la Terre, généralement causée par un séisme.
    Dans cette application, nous visualisons une onde sismique captee par une station japonaise.
    """
)
time= np.linspace(0, 120, 12000)  

import numpy as np

# Création du vecteur temps (exemple pour 2 minutes à 100 Hz)
time = np.linspace(0, 120, 120*100)

def generate_wave(time, wave_type, start, end):
    sig = np.zeros_like(time)
    
    # Création d'une fenêtre de Hanning pour l'enveloppe
    window_length = int(len(time) * (end-start)/time[-1])
    if window_length > 0:
        hanning_win = sp.signal.windows.hann(window_length * 2)     
        win_start = max(0, int(len(time)*start/time[-1]) - window_length//2)
        win_end = min(len(time), int(len(time)*end/time[-1]) + window_length//2)
        full_window = np.zeros_like(time)
        full_window[win_start:win_end] = hanning_win[:win_end-win_start]
    else:
        full_window = np.ones_like(time)

    if wave_type == 'P':
        # Ondes P 
        for i in range(1000):
            freq = 10 + np.random.normal(0, 1) #10hz
            amp = 10 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)
    
    elif wave_type == 'S':
        # Ondes S
        for i in range(1000):
            freq = 1 + np.random.normal(0, 0.5) #1hz
            amp = 20 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)
    
    elif wave_type == 'surface':
        # Ondes de surface
        for i in range(1000): 
            freq = 2 + np.random.normal(0, 0.1)
            amp = 50 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)

    return sig

# Génération des composantes
def generate_seismic_signal(time,start_p, end_p, start_s, end_s, start_surface, end_surface):
    # Bruit de fond
    noise = np.random.normal(0, 0.1, len(time))
    
    # Génération des ondes
    p_wave = generate_wave(time, 'P', start_p, end_p)  
    s_wave = generate_wave(time, 'S', start_s, end_s)
    surface_wave = generate_wave(time, 'surface', start_surface, end_surface)

    # Composition des signaux par composante
    signal_x = noise + 0.1*p_wave + 0.7*s_wave + 0.4*surface_wave
    signal_y = noise + 0.1*p_wave + 0.9*s_wave + 0.5*surface_wave
    signal_z = noise + 1.0*p_wave + 0.1*s_wave + 0.4*surface_wave
    
    return signal_x, signal_y, signal_z

# Génération des signaux
@st.cache_data
def get_signal():
    time = np.linspace(0, 120, 120*100)
    signal_x, signal_y, signal_z = generate_seismic_signal(time, 15, 30, 35, 50, 60, 100)
    return signal_x, signal_y, signal_z
signal_x, signal_y, signal_z = get_signal()

# Création du graphique

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=time, y=signal_x+signal_y+signal_z, mode='lines', name='Signal combiné',line=dict(color='purple')))
fig1.update_layout(
    title="Signal combiné (X + Y + Z)",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
) 
st.plotly_chart(fig1, use_container_width=True)

st.subheader("""Comparaison le temps de depart des signaux X, Y et Z""")

# Création de la figure avec subplots liés
fig_combined = make_subplots(
    rows=3, cols=1,
    subplot_titles=("Composante Nord-Sud (X)", "Composante Est-Ouest (Y)", "Composante Verticale (Z)"),
    vertical_spacing=0.1,
    shared_xaxes=True  # Ceci synchronise le zoom horizontal
)

# Ajout des traces
fig_combined.add_trace(
    go.Scatter(x=time, y=signal_x, mode='lines', name='X', line=dict(color='blue')),
    row=1, col=1
)

fig_combined.add_trace(
    go.Scatter(x=time, y=signal_y, mode='lines', name='Y', line=dict(color='red')),
    row=2, col=1
)

fig_combined.add_trace(
    go.Scatter(x=time, y=signal_z, mode='lines', name='Z', line=dict(color='lime')),
    row=3, col=1
)

# Configuration du layout
fig_combined.update_layout(
    height=900,
    showlegend=False,
    template="plotly_white",
    xaxis=dict(matches='x2'),
    xaxis2=dict(matches='x3')
)

# Configuration des axes
fig_combined.update_xaxes(title_text="Temps (s)", row=3, col=1)
fig_combined.update_yaxes(title_text="Amplitude X", row=1, col=1)
fig_combined.update_yaxes(title_text="Amplitude Y", row=2, col=1)
fig_combined.update_yaxes(title_text="Amplitude Z", row=3, col=1)

fig_combined.update_layout(
    title="Comparaison des signaux sismiques (X, Y, Z)",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)

st.plotly_chart(fig_combined, use_container_width=True)

st.write(
    """
    On peut remarquer que le signal nord-sud (X) et le signal est-ouest (Y) ont un temps de départ similaire, tandis que le signal vertical (Z) a un temps de départ différent.
    Cela est dû à la nature des ondes sismiques qui se propagent différemment dans les différentes directions.
    """
)

st.header("2. Écoute du signal sismique")   

st.write("""
    On peut écouter le signal sismique en cliquant sur le bouton ci-dessous.
""")

audio_signal = np.array(signal_x + signal_y + signal_z)
audio_signal = audio_signal.astype(np.float32)
audio_signal /= np.max(np.abs(audio_signal))
audio_signal =audio_signal*5

sample_rate = 3000
st.write("Le signal est acceleré pour qu'on puisse l'écouter .")

st.audio(audio_signal, sample_rate=sample_rate)

acceleration_factor = sample_rate/ 100  # Accélération du signal pour l'écouter

st.write(f"✅ Le signal a été accéléré d’un facteur {acceleration_factor:.1f} pour être écoutable.")


st.header("3. Détection des ondes P et S dans les signaux sismiques avec l'énergie ")

def bandpass_filter(data, lowcut, highcut, fs, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sp.signal.butter(order, [low, high], btype='band')
    return sp.signal.filtfilt(b, a, data)

# Calcul de l'énergie de l'enveloppe du signal
def compute_energy_envelope(filtered_signal, fs, window_sec=0.5):
    window_size = int(window_sec * fs)
    energy = np.convolve(np.abs(filtered_signal)**2, np.ones(window_size), mode='same')
    return energy / np.max(energy)  # normalisé


st.write(
    """    Dans cette section, nous allons détecter les ondes P et S dans les signaux sismiques captés par la station.
    Les ondes P (primaires) sont des ondes de compression qui se déplacent plus rapidement que les ondes S (secondaires), qui sont des ondes de cisaillement.
    Nous allons isoler les fréquences typiques de ces ondes.
    Et nous allons visualiser l'énergie du signal pour identifier les pics correspondant aux ondes P et S et détecter leur arrivée dans le signal.
    """)

fs = 110  # fréquence d'échantillonnage


st.write(
    """Nous allons filtrer les signaux pour détecter les ondes P et S.
    ondes P : environ 10 Hz (fréquence typique)
    ondes S : environ 1 Hz (fréquence typique)
    """
)
st.write(
    """Pour chaque signal (Nord-Sud, Est-Ouest, Vertical), nous allons :
    1. Appliquer un filtre passe-bande pour isoler les fréquences des ondes P et S.
    2. Calculer l'énergie de l'enveloppe du signal filtré.
    3. Détecter les pics dans l'énergie de l'enveloppe pour identifier les moments d'arrivée des ondes P et S.
    """
)
st.write(
    """Selection la bande de frequence pour les ondes P et S :
    """
)

f_min_p, f_max_p = st.slider(
        "Bande de fréquence pour l'onde P (en Hz)",
        min_value=0.0,
        max_value=50.0,
        value=(0.1, 50.0),
        step=0.1,
        key='slider_p'
    )

f_min_s, f_max_s = st.slider(
        "Bande de fréquence pour l'onde S (en Hz)",
        min_value=0.1,
        max_value=50.0,
        value=(0.1, 50.0),
        step=0.1,
        key='slider_s'
    )
if st.button("Indice pour un bon choix des bandes de fréquence"):
    st.info("la bande de fréquence pour l'onde P doit être centree autour de 10 Hz et pour l'onde S autour de 1 Hz.")
    st.info("on peut utiliser comme bande de fréquence pour l'onde P : 8-12 Hz et pour l'onde S : 0.5-2 Hz.")

st.write(
    """ Choisissez le signal à analyser :
    """)
signal_choice = st.selectbox("Sélectionnez le signal", ("Nord-Sud", "Est-Ouest", "Vertical"))

if signal_choice == "Nord-Sud":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_x = go.Figure()
    signal_s = bandpass_filter(signal_x, f_min_s, f_max_s, fs)  # Onde S

    energie_s = compute_energy_envelope(signal_s, fs)

    
    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_s_x=st.slider(
        "Temps d'arrivée de l'onde S (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="cyan", annotation_text="Onde S")

    if st.button("Verification des temps d'arrivée de l'onde S"):
        signal_s = bandpass_filter(signal_x, 0.5, 2, fs)  # Onde S

        energie_s = compute_energy_envelope(signal_s, fs)

        # Détection de pics
        peaks_s, _ = sp.signal.find_peaks(energie_s, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='blue')))
        
        if  len(peaks_s) > 0:
            t_s_x = time[peaks_s[0]]

            
            st.success(f"🟣 Onde S détectée à t = {t_s_x:.2f} s (≈1 Hz)")

            fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="purple", annotation_text="Onde S")
            

        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_x, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='blue')))
        st.plotly_chart(fig_puissance_x, use_container_width=True)

    

if signal_choice == "Est-Ouest":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_y = go.Figure()
    signal_s = bandpass_filter(signal_y, f_min_s, f_max_s, fs)  # Onde S

    energie_s = compute_energy_envelope(signal_s, fs)

    
    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_s_y=st.slider(
        "Temps d'arrivée de l'onde S (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_y.add_vline(x=t_s_y, line_dash="dash", line_color="orange", annotation_text="Onde S")
    if st.button("Verification des temps d'arrivée de l'onde S"):
        signal_s = bandpass_filter(signal_y, 0.5, 2, fs)  # Onde S

        energie_s = compute_energy_envelope(signal_s, fs)

        # Détection de pics
        peaks_s, _ = sp.signal.find_peaks(energie_s, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='red')))

        if  len(peaks_s) > 0:
            t_s_y = time[peaks_s[0]]


            st.success(f"🟣 Onde S détectée à t = {t_s_y:.2f} s (≈1 Hz)")

            fig_puissance_y.add_vline(x=t_s_y, line_dash="dash", line_color="purple", annotation_text="Onde S")


        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_y, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='red')))
        st.plotly_chart(fig_puissance_y, use_container_width=True)


if signal_choice == "Vertical":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_z = go.Figure()
    signal_p = bandpass_filter(signal_z, f_min_p, f_max_p, fs)  # Onde S

    energie_p = compute_energy_envelope(signal_p, fs)

    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_p_z=st.slider(
        "Temps d'arrivée de l'onde P (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_z.add_vline(x=t_p_z, line_dash="dash", line_color="yellow", annotation_text="Onde P")
    if st.button("Verification des temps d'arrivée de l'onde P"):
        signal_p = bandpass_filter(signal_z, 8, 12, fs)  # Onde P

        energie_p = compute_energy_envelope(signal_p, fs)

        # Détection de pics
        peaks_p, _ = sp.signal.find_peaks(energie_p, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='green')))

        if  len(peaks_p) > 0:
            t_p_x = time[peaks_p[0]]


            st.success(f"🟢 Onde P détectée à t = {t_p_x:.2f} s (≈10 Hz)")

            fig_puissance_z.add_vline(x=t_p_x, line_dash="dash", line_color="lime", annotation_text="Onde P")


        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_z, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='green')))
        st.plotly_chart(fig_puissance_z, use_container_width=True)


st.write("""notez les temps d'arrivée des ondes P et S """)
st.info(f"Temps d'arrivée de l'onde S prenons la moyenne des deux temps : (t_s_x + t_s_y)/2 s")
t_p=st.number_input(
    "Temps d'arrivée de l'onde P (en secondes)",
    min_value=float(time[0]),
    max_value=float(time[-1]),
    value=(float(time[0])),
    step=0.1,
    key='input_tp'
)
t_s=st.number_input(
    "Temps d'arrivée de l'onde S (en secondes)",
    min_value=float(time[0]),
    max_value=float(time[-1]),
    value=(float(time[0])),
    step=0.1,
    key='input_ts'
)





if st.button("Calculer la distance à l'épicentre du séisme"):
    st.header("4. Calcul de la distance à l'épicentre du séisme")
    st.write(
        """
        En utilisant les temps d'arrivée des ondes P et S, nous pouvons estimer la distance à l'épicentre du séisme.
        La vitesse des ondes P est d'environ 7.3 km/s et celle des ondes S est d'environ 3 km/s.
        La distance à l'épicentre peut être estimée en utilisant la formule :
        $D = \\frac{{Δt}}{{\\frac{{1}}{{V_s}} - \\frac{{1}}{{V_p}}}} = \\frac{{V_p × V_s}}{{V_p - V_s}} × Δt$
        où $Δt = t_s - t_p$ est la différence de temps d'arrivée des ondes S et P.
        """
    )

    st.write(f"Temps d'arrivée de l'onde P : {t_p:.2f} s")
    st.write(f"Temps d'arrivée de l'onde S : {t_s:.2f} s")

    if t_s > t_p and t_s > 0 and t_p > 0:
        st.success("Les temps d'arrivée des ondes P et S sont valides.")
    else:
        st.error("Les temps d'arrivée des ondes P et S ne sont pas valides. Veuillez vérifier les valeurs saisies.")

    if t_s > t_p and t_s > 0 and t_p > 0:

        Vp = 7.3  # Vitesse des ondes P en km/s
        Vs = 3.0  # Vitesse des ondes S en km/s
        delta_t = t_s - t_p  # Différence de temps d'arrivée des ondes S et P
        D = (Vp * Vs) / (Vp - Vs) * delta_t  # Distance à l'épicentre en km

        st.markdown(f"La distance à l'épicentre du séisme est d'environ {D:.2f} km.")
        st.write(
            """
            Cette distance est une estimation basée sur les temps d'arrivée des ondes P et S et les vitesses typiques de ces ondes.
            Elle peut varier en fonction des conditions géologiques et de la profondeur du séisme.
            """
        )

