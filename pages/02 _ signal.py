import numpy as np
import streamlit as st
import plotly.graph_objects as go
import scipy as sp

st.set_page_config(page_title="Signal Sinusoïdal", page_icon=":musical_note:", layout="wide")

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
st.write("### Paramètres du signal")
col1, col2, col3 = st.columns(3)
with col1:
    A = st.slider("Amplitude (A)", min_value=1.0, max_value=10.0, value=1.0, step=0.5)
with col2:
    f = st.slider("Fréquence (f)", min_value=1, max_value=100, value=1, step=1)
with col3:
    phi = st.slider("Phase (φ en radians)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f")

t = np.linspace(0, 3, 3000)
y = A * np.cos(2 * np.pi * f * t + phi)

col1, col2 = st.columns(2)

with col1:
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

with col2:
    
    N = len(t)
    frequences = np.fft.fftfreq(N, d=(t[1]-t[0]))[:N//2]  
    amplitude = np.abs(np.fft.fft(y))[:N//2] * 2/N 

    # Détection des pics dans le spectre
    peaks = (np.abs(amplitude) > 0.8)  # Seuil arbitraire

    fig_fft = go.Figure()

    fig_fft.add_trace(go.Scatter(x=frequences, y=np.zeros_like(frequences),  
                            line=dict(color='white')))

    # Marquage des pics
    fig_fft.add_trace(go.Scatter(x=frequences[peaks], y=amplitude[peaks],
                            mode='markers',
                            marker=dict(color='red', size=4)))

    for freq, amp in zip(frequences[peaks], amplitude[peaks]):
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
                    xaxis_range=[0, f*1.05],
                    showlegend=False)


    st.plotly_chart(fig_fft, use_container_width=True)


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


st.plotly_chart(fig_fft, use_container_width=True, key="spectre_signal")


st.header("3. Puissance d'un signal : explication visuelle")
st.write(
    """
    La **puissance instantanée** correspond au carré du signal à chaque instant.
    Plus la courbe orange est haute, plus le signal est puissant à cet instant.
    """
)
y2 = y**2
fig_puissance = go.Figure()
fig_puissance.add_trace(go.Scatter(x=t, y=y2, mode='lines', name='Puissance instantanée', line=dict(color='orange')))
fig_puissance.update_layout(
    title="Puissance instantanée du signal",
    xaxis_title="Temps (t)",
    yaxis_title="Puissance instantanée",
    template="plotly_white"
)
st.plotly_chart(fig_puissance, use_container_width=True,key="puissance_signal")



# Création d'un signal cosinus avec fréquence variable
st.header("Exemple avec un cosinus")


# Paramètres
f_max = 11000  # Fréquence maximale
A = st.slider("Amplitude (A)", 0.1, 2.0, 1.0)
f = st.slider("Fréquence (f)",0, f_max, 1000, step=10)  # Fréquence du signal




time = np.linspace(0, 3, 132000)  # Temps de 0 à 3 secondes

carrier = A * np.cos(2*np.pi*f*time)

# Initialiser les états dans la session si besoin
if "add_500hz" not in st.session_state:
    st.session_state["add_500hz"] = False
if "add_300hz" not in st.session_state:
    st.session_state["add_300hz"] = False
if "add_6000hz" not in st.session_state:
    st.session_state["add_6000hz"] = False
if "add_10000hz" not in st.session_state:
    st.session_state["add_10000hz"] = False

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Ajouter un signal à 500 Hz"):
        st.session_state["add_500hz"] = not st.session_state["add_500hz"]

with col2:
    if st.button("Ajouter un signal à 6000 Hz"):
        st.session_state["add_6000hz"] = not st.session_state["add_6000hz"]

with col3:
    if st.button("Ajouter un signal à 10000 Hz"):
        st.session_state["add_10000hz"] = not st.session_state["add_10000hz"]

with col4:
    if st.button("Ajouter un signal à 300 Hz"):
        st.session_state["add_300hz"] = not st.session_state["add_300hz"]

if "add_noise" not in st.session_state:
    st.session_state["add_noise"] = False

if st.button("Ajouter du bruit blanc"):
    st.session_state["add_noise"] = not st.session_state["add_noise"]

#Formule du signal avec les signaux additionnels et valeurs 
st.subheader("Formule du signal")
formule = f"x(t) = {A} * cos(2π * {f} * t)"

# Génération des signaux selon l'état
if st.session_state["add_6000hz"]:
    A1 = st.slider("Amplitude du signal à 6000 Hz", 0.1, 2.0, 0.5, step=0.1)
    c1 = A1 * np.cos(2 * np.pi * 6000 * time)
    formule += f" + {A1} * cos(2π * 6000 * t)"
else:
    c1 = np.zeros_like(time)

if st.session_state["add_300hz"]:
    A2 = st.slider("Amplitude du signal à 300 Hz", 0.1, 2.0, 1.0, step=0.1)
    c2 = A2 * np.cos(2 * np.pi * 300 * time)
    formule += f" + {A2} * cos(2π * 300 * t)"
else:
    c2 = np.zeros_like(time)

if st.session_state["add_10000hz"]:
    A3 = st.slider("Amplitude du signal à 10000 Hz", 0.1, 2.0, 1.5, step=0.1)
    c3 = A3 * np.cos(2 * np.pi * 10000 * time)
    formule += f" + {A3} * cos(2π * 10000 * t)"
else:
    c3 = np.zeros_like(time)

if st.session_state["add_500hz"]:
    A4 = st.slider("Amplitude du signal à 500 Hz", 0.1, 2.0, 1.0, step=0.1)
    c4 = A4 * np.cos(2 * np.pi * 500 * time)
    formule += f" + {A4} * cos(2π * 500 * t)"
else:
    c4 = np.zeros_like(time)

#Bouton bruit


if st.session_state["add_noise"]:
    A_noise = st.slider("Amplitude du bruit", 0.0, 1.0, 0.01, step=0.01)
    noise =  np.random.normal(0, A_noise, size=time.shape)  # Bruit blanc
    formule +=" + bruit"
else:
    noise = np.zeros_like(time)

x = carrier + c1 + c2 + c3 + c4 + noise

#formule de signal
st.write(formule)


# Bouton pour activer/désactiver le son
st.subheader("Activer/Désactiver le son")

if "play_audio" not in st.session_state:
    st.session_state["play_audio"] = False  

if st.button("Activer/Désactiver le son"):
    st.session_state["play_audio"] = not st.session_state["play_audio"]

col1, col2 = st.columns(2)
with col1:
    st.subheader("Signal généré")
    st.write("Voici le signal généré avec les paramètres et options sélectionnés.")
    # Visualisation
    fig = go.Figure()

    # Signal temporel (affichage selon l'intervalle choisi)
    mask = (time >= 0) & (time <= 100/f_max)  # Afficher de 0 à 1/f_max secondes
    fig.add_trace(go.Scatter(
        x=time[mask], y=x[mask],
        mode='lines',
        name='Signal',
        line=dict(color='blue', width=1)
    ))

    fig.update_layout(
        title="Signal cosinus à fréquence variable",
        xaxis_title="Temps (s)",
        xaxis_range=[0, 100/f_max],
        yaxis_title="Amplitude"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Spectre du signal")
    st.write("Voici le spectre du signal, montrant les fréquences présentes dans le signal généré.")
    # Spectre du signal
    N = len(x)
    frequences = np.fft.fftfreq(N, d=(time[1]-time[0]))[:N//2]  
    amplitude = np.abs(np.fft.fft(x))[:N//2] * 2/N 

    fig_spectre = go.Figure()
    fig_spectre.add_trace(go.Scatter(
        x=frequences, y=amplitude,
        mode='lines',
        name='Spectre',
        line=dict(color='red', width=1)
    ))
    fig_spectre.update_layout(
        title="Spectre du signal",
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Amplitude",
        xaxis_range=[0, f_max],
        template='plotly_white'
    )

    st.plotly_chart(fig_spectre, use_container_width=True)

sample_rate = 44000

if st.session_state["play_audio"]:
    st.audio(x, sample_rate=sample_rate, loop=True)

st.subheader("Caractéristisation des ondes sismiques")

st.write("""
Les ondes sismiques sont des vibrations provoquées par un séisme ou une explosion. Elles se propagent à travers la Terre selon différents modes, que l'on classe en trois grandes catégories :
""")

st.markdown("### 🌊 Types d'ondes sismiques")

# Crée un tableau comparatif
st.table({
    "Type d'onde": ["P (Primaire)", "S (Secondaire)", "Ondes de surface (Love & Rayleigh)"],
    "Nature": ["Longitudinale", "Transversale", "Mixte (transversale + déplacement vertical/horizontal)"],
    "Vitesse (km/s)": ["7.3", "4", "1–4"],
    "Fréquences typiques": ["Environ 10 Hz", "Environ 1 Hz", "0.005 – 5 Hz"],
    "Amplitude relative": ["Faible", "Moyenne", "**Forte** "],
    "Effet sur les bâtiments": [
        "Vibrations rapides, peu destructrices",
        "Oscillations plus fortes, plus destructrices",
        "**Très destructrices** sur grandes structures"
    ]
})

st.markdown("### 🚀 Résumé visuel")
st.write("""
- ✅ **Ondes P** : premières à arriver, se propagent vite, compression/dilatation.
- ✅ **Ondes S** : arrivent ensuite, vibrent perpendiculairement à la direction de propagation.
- ✅ **Ondes de surface** : arrivent en dernier, mais provoquent le plus de dégâts.

**Note :** Les sismographes enregistrent souvent d'abord les ondes P, puis les S, puis les ondes de surface.

""")

