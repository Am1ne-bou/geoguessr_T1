import numpy as np
import plotly.graph_objects as go
import streamlit as st
import scipy as sp
import matplotlib.pyplot as plt

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


time=np.linspace(0, 120, len(signal_5))

for i in range(len(signal_5)):
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
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=time, y=signal_x+signal_y+signal_z, mode='lines', name='Signal combiné',line=dict(color='purple')))
fig1.update_layout(
    title="Signal combiné (X + Y + Z)",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
) 
st.plotly_chart(fig1, use_container_width=True)

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

st.header("2. Quiz rapide")
st.write(
    """
    Répondez aux questions suivantes pour tester vos connaissances sur les ondes sismiques.
    """
)
question1 = st.radio(
    "Quelle est la différence principale entre les ondes P et S ?",
    [
        "Les ondes P sont plus rapides que les ondes S.",
        "Les ondes S sont plus rapides que les ondes P.",
        "Les ondes P et S ont la même vitesse."
    ]
)
if st.button("Vérifier ma réponse 1"):
    if question1 == "Les ondes P sont plus rapides que les ondes S.":
        st.success("Bravo ! C’est la bonne réponse.")
    else:
        st.error("Ce n'est pas la bonne réponse. Essayez encore !")

question2 = st.radio(
    "Quel type de mouvement les ondes P provoquent-elles dans le sol ?",
    [
        "Mouvement vertical",
        "Mouvement horizontal",
        "Mouvement circulaire"
    ]
)
if st.button("Vérifier ma réponse 2"):
    if question2 == "Mouvement vertical":
        st.success("Bravo ! C’est la bonne réponse.")
    else:
        st.error("Ce n'est pas la bonne réponse. Essayez encore !")

question3 = st.radio(
    "Quel type de mouvement les ondes S provoquent-elles dans le sol ?",
    [
        "Mouvement vertical",
        "Mouvement horizontal",
        "Mouvement circulaire"
    ]
)

if st.button("Vérifier ma réponse 3"):
    if question3 == "Mouvement horizontal":
        st.success("Bravo ! C’est la bonne réponse.")
    else:
        st.error("Ce n'est pas la bonne réponse. Essayez encore !")

#écouter le signal
st.write("""
    On peut écouter le signal sismique en cliquant sur le bouton ci-dessous.
""")

audio_signal = np.array(signal_x + signal_y + signal_z)
audio_signal = audio_signal.astype(np.float32)
audio_signal /= np.max(np.abs(audio_signal))
audio_signal =audio_signal*5

sample_rate = 12000
st.write("Le signal est acceleré pour qu'on puisse l'écouter .")

st.audio(audio_signal, sample_rate=sample_rate)

acceleration_factor = sample_rate/ 100  # Accélération du signal pour l'écouter

st.write(f"✅ Le signal a été accéléré d’un facteur {acceleration_factor:.1f} pour être écoutable.")

st.header("3. Spectrogramme de l'onde sismique")
st.write(
    """on utilise le spectrogramme pour visualiser comment les fréquences du signal évoluent dans le temps.
    On va l'utiliser pour analyser les signaux captés par la station sismique.Et pour detreminer quand les ondes P et S sont arrivées.
    """
)
tab4,tab5,tab6 = st.tabs(["Signal nord_sud (X)", "Signal est_ouest (Y)", "Signal vertical (Z)"])


with tab4:
    # Calcul du spectrogramme
    f_spec_x, t_spec_x, Sxx = sp.signal.spectrogram(np.array(signal_x), fs=100, nperseg=256, noverlap=255)

    # Sélection de l'intervalle de temps à afficher
    st.subheader("Choisissez l'intervalle de temps à afficher")
    t_min_x, t_max_x= st.slider(
        "Intervalle de temps (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0]), float(time[-1])),
        step=0.1,key='slider_x'
    )

    # Visualisation
    fig = go.Figure()

    # Signal temporel (affichage selon l'intervalle choisi)
    mask = (t_spec_x >= t_min_x) & (t_spec_x <= t_max_x)

    # Création du graphique du spectrogramme
    fig_spec = go.Figure(data=go.Heatmap(
        z=Sxx[:,mask],
        x=t_spec_x[mask],
        y=f_spec_x,
        colorscale='Turbo',  
        colorbar=dict(title='Puissance '),
        zsmooth='best'
    ))

    fig_spec.update_layout(
        title="Spectrogramme interactif - Onde sismique (Nord-Sud)",
        xaxis=dict(
            title="Temps (s)",
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        yaxis=dict(
            title="Fréquence (Hz)",
            range=[0, 25],  # Limiter la bande utile (par ex. 0-25 Hz)
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        margin=dict(l=60, r=20, t=50, b=50),
        height=500,
        template="plotly_white"
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig_spec, use_container_width=True)

with tab5:
    # Calcul du spectrogramme
    f_spec_y, t_spec_y, Syy = sp.signal.spectrogram(np.array(signal_y), fs=100, nperseg=256, noverlap=255)

    # Sélection de l'intervalle de temps à afficher
    st.subheader("Choisissez l'intervalle de temps à afficher")
    t_min_y, t_max_y = st.slider(
        "Intervalle de temps (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0]), float(time[-1])),
        step=0.1,key='slider_y'
    )

    # Visualisation
    fig = go.Figure()

    # Signal temporel (affichage selon l'intervalle choisi)
    mask = (t_spec_y >= t_min_y) & (t_spec_y <= t_max_y)

    # Création du graphique du spectrogramme
    fig_spec = go.Figure(data=go.Heatmap(
        z=Syy[:,mask],
        x=t_spec_y[mask],
        y=f_spec_y,
        colorscale='Turbo',
        colorbar=dict(title='Puissance '),
        zsmooth='best'
    ))

    fig_spec.update_layout(
        title="Spectrogramme interactif - Onde sismique (Est-Ouest)",
        xaxis=dict(
            title="Temps (s)",
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        yaxis=dict(
            title="Fréquence (Hz)",
            range=[0, 25],  # Limiter la bande utile (par ex. 0-25 Hz)
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        margin=dict(l=60, r=20, t=50, b=50),
        height=500,
        template="plotly_white"
    )

    # Affichage dans Streamlit
    st.plotly_chart(fig_spec, use_container_width=True)

with tab6:
    # Calcul du spectrogramme
    f_spec_z, t_spec_z, Szz = sp.signal.spectrogram(np.array(signal_z), fs=100, nperseg=256, noverlap=255)

    # Sélection de l'intervalle de temps à afficher
    st.subheader("Choisissez l'intervalle de temps à afficher")
    t_min_z, t_max_z = st.slider(
        "Intervalle de temps (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0]), float(time[-1])),
        step=0.1, key='slider_z'
    )

    # Visualisation
    fig = go.Figure()

    
    mask = (t_spec_z >= t_min_z) & (t_spec_z <= t_max_z)

    # Création du graphique du spectrogramme
    fig_spec = go.Figure(data=go.Heatmap(
        z=Szz[:,mask],
        x=t_spec_z[mask],
        y=f_spec_z,
        colorscale='Turbo',
        colorbar=dict(title='Puissance '),
        zsmooth='best'
    ))

    fig_spec.update_layout(
        title="Spectrogramme interactif - Onde sismique (Vertical)",
        xaxis=dict(
            title="Temps (s)",
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        yaxis=dict(
            title="Fréquence (Hz)",
            range=[0, 25],  # Limiter la bande utile (par ex. 0-25 Hz)
            showgrid=True,
            gridcolor='rgba(200,200,200,0.2)'
        ),
        font=dict(
            family="Arial",
            size=14
        ),
        margin=dict(l=60, r=20, t=50, b=50),
        height=500,
        template="plotly_white"
    )

    st.plotly_chart(fig_spec, use_container_width=True)

def bandpass_filter(data, lowcut, highcut, fs, order=4):
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

st.header("4. Détection des ondes P et S")
st.write(
    """    Dans cette section, nous allons détecter les ondes P et S dans les signaux sismiques captés par la station.
    Les ondes P (primaires) sont des ondes de compression qui se déplacent plus rapidement que les ondes S (secondaires), qui sont des ondes de cisaillement.
    Nous allons utiliser un filtre passe-bande pour isoler les fréquences typiques de ces ondes.
    Et nous allons visualiser l'énergie de l'enveloppe du signal pour identifier les pics correspondant aux ondes P et S et détecter leur arrivée dans le signal.
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
    signal_p = bandpass_filter(signal_x, f_min_p, f_max_p, fs)   # Onde P
    signal_s = bandpass_filter(signal_x, f_min_s, f_max_s, fs)  # Onde S

    energie_p = compute_energy_envelope(signal_p, fs)
    energie_s = compute_energy_envelope(signal_s, fs)

    
    # Traces de l’énergie et des pics
    fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='green')))
    fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='purple')))

    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur
    t_p_x=st.slider(
        "Temps d'arrivée de l'onde P (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_tp'
    )
    t_s_x=st.slider(
        "Temps d'arrivée de l'onde S (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )

    if st.button("Verification des temps d'arrivée des ondes P et S"):
        signal_p = bandpass_filter(signal_x, 8, 12, fs)   # Onde P
        signal_s = bandpass_filter(signal_x, 0.5, 2, fs)  # Onde S

        energie_p = compute_energy_envelope(signal_p, fs)
        energie_s = compute_energy_envelope(signal_s, fs)

        # Détection de pics
        peaks_p, _ = sp.signal.find_peaks(energie_p, height=0.1, distance=int(0.3 * fs))
        peaks_s, _ = sp.signal.find_peaks(energie_s, height=0.1, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='lime')))
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='blue')))
        
        if len(peaks_p) > 0 and len(peaks_s) > 0:
            t_p_x = time[peaks_p[0]]
            t_s_x = time[peaks_s[0]]

            st.success(f"🟢 Onde P détectée à t = {t_p_x:.2f} s (≈10 Hz)")
            st.success(f"🟣 Onde S détectée à t = {t_s_x:.2f} s (≈1 Hz)")

            fig_puissance_x.add_vline(x=t_p_x, line_dash="dash", line_color="green", annotation_text="Onde P")
            fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="purple", annotation_text="Onde S")
            

        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_x, use_container_width=True)

    else:
        fig_puissance_x.add_vline(x=t_p_x, line_dash="dash", line_color="green", annotation_text="Onde P")
        fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="purple", annotation_text="Onde S")
        st.plotly_chart(fig_puissance_x, use_container_width=True)

    

if signal_choice == "Est-Ouest":
    fig_puissance_y = go.Figure()
    # Filtrage dans les bandes typiques des ondes P et S
    signal_p_y = bandpass_filter(signal_y, 8, 12, fs)   # Onde P ~10 Hz
    signal_s_y = bandpass_filter(signal_y, 0.5, 2, fs)  # Onde S ~1 Hz
    energie_p_y = compute_energy_envelope(signal_p_y, fs)
    energie_s_y = compute_energy_envelope(signal_s_y, fs)
    # Détection de pics
    peaks_p_y, _ = sp.signal.find_peaks(energie_p_y, height=0.1, distance=int(0.3 * fs))
    peaks_s_y, _ = sp.signal.find_peaks(energie_s_y, height=0.1, distance=int(0.3 * fs))
    # Traces de l’énergie et des pics
    fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_p_y, mode='lines', name='Énergie onde P', line=dict(color='green')))
    fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_s_y, mode='lines', name='Énergie onde S', line=dict(color='purple')))    
    if len(peaks_p_y) > 0 and len(peaks_s_y) > 0:
        t_p_y = time[peaks_p_y[0]]
        t_s_y = time[peaks_s_y[0]]

        st.success(f"🟢 Onde P détectée à t = {t_p_y:.2f} s (≈10 Hz)")
        st.success(f"🟣 Onde S détectée à t = {t_s_y:.2f} s (≈1 Hz)")

        fig_puissance_y.add_vline(x=t_p_y, line_dash="dash", line_color="green", annotation_text="Onde P")
        fig_puissance_y.add_vline(x=t_s_y, line_dash="dash", line_color="purple", annotation_text="Onde S")
    else:
        st.warning("Impossible de détecter automatiquement les ondes P et S.")
    # Affichage final
    st.plotly_chart(fig_puissance_y, use_container_width=True)

if signal_choice == "Vertical":
    fig_puissance_z = go.Figure()
    # Filtrage dans les bandes typiques des ondes P et S
    signal_p_z = bandpass_filter(signal_z, 8, 12, fs)   # Onde P ~10 Hz
    signal_s_z = bandpass_filter(signal_z, 0.5, 2, fs)  # Onde S ~1 Hz
    energie_p_z = compute_energy_envelope(signal_p_z, fs)
    energie_s_z = compute_energy_envelope(signal_s_z, fs)
    # Détection de pics
    peaks_p_z, _ = sp.signal.find_peaks(energie_p_z, height=0.1, distance=int(0.3 * fs))
    peaks_s_z, _ = sp.signal.find_peaks(energie_s_z, height=0.1, distance=int(0.3 * fs))
    # Traces de l’énergie et des pics
    fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_p_z, mode='lines', name='Énergie onde P', line=dict(color='green')))
    fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_s_z, mode='lines', name='Énergie onde S', line=dict(color='purple')))
    if len(peaks_p_z) > 0 and len(peaks_s_z) > 0:
        t_p_z = time[peaks_p_z[0]]
        t_s_z = time[peaks_s_z[0]]

        st.success(f"🟢 Onde P détectée à t = {t_p_z:.2f} s (≈10 Hz)")
        st.success(f"🟣 Onde S détectée à t = {t_s_z:.2f} s (≈1 Hz)")

        fig_puissance_z.add_vline(x=t_p_z, line_dash="dash", line_color="green", annotation_text="Onde P")
        fig_puissance_z.add_vline(x=t_s_z, line_dash="dash", line_color="purple", annotation_text="Onde S")
    else:
        st.warning("Impossible de détecter automatiquement les ondes P et S.")
    # Affichage final
    st.plotly_chart(fig_puissance_z, use_container_width=True)


