import numpy as np
import streamlit as st
import plotly.graph_objects as go
import scipy as sp
import matplotlib.pyplot as plt

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

A = st.slider("Amplitude (A)", min_value=0.0, max_value=10.0, value=1.0, step=0.5)
f = st.slider("Fréquence (f)", min_value=4.0    , max_value=15.0, value=1.0, step=0.1)
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
amplitude = np.abs(np.fft.fft(y))[:N//2] * 2/N 

# Détection des pics dans le spectre
peaks = (np.abs(amplitude) > 0.1)  # Seuil arbitraire

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
st.plotly_chart(fig_puissance, use_container_width=True)

st.title("Introduction au Spectrogramme")
st.markdown("""
## Qu'est-ce qu'un spectrogramme ?

Un **spectrogramme** est une représentation visuelle qui montre :
- **Comment les fréquences** d'un signal **évoluent dans le temps**
- **L'intensité** (puissance) de chaque fréquence à chaque instant

C'est comme une "carte thermique" des fréquences !
""")

# Création d'un signal cosinus avec fréquence variable
st.header("Exemple avec un cosinus")
st.markdown("Un signal simple : $x(t) = A\cos(2\pi f) t)$ où $f(t)$ change au cours du temps")

# Paramètres
f_max = 100  # Fréquence maximale
A = st.slider("Amplitude (A)", 0.1, 2.0, 1.0)
f = st.slider("Fréquence (f)",0, f_max, 10, step=1)  # Fréquence du signal


fs = 2*10e1  # Fréquence d'échantillonnage
N = 1e5  # Nombre d'échantillons

time = np.arange(N) / float(fs)

carrier = A * np.cos(2*np.pi*f*time)

# Initialiser les états dans la session si besoin
if "add_5hz" not in st.session_state:
    st.session_state["add_5hz"] = False
if "add_30hz" not in st.session_state:
    st.session_state["add_30hz"] = False
if "add_60hz" not in st.session_state:
    st.session_state["add_60hz"] = False
if "add_15hz" not in st.session_state:
    st.session_state["add_15hz"] = False

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Ajouter un signal à 5 Hz\n(0-200 s)"):
        st.session_state["add_5hz"] = not st.session_state["add_5hz"]

with col2:
    if st.button("Ajouter un signal à 60 Hz\n(150-250 s)"):
        st.session_state["add_60hz"] = not st.session_state["add_60hz"]

with col3:
    if st.button("Ajouter un signal à 15 Hz\n(400-500 s)"):
        st.session_state["add_15hz"] = not st.session_state["add_15hz"]

with col4:
    if st.button("Ajouter un signal à 30 Hz\n(450-500 s)"):
        st.session_state["add_30hz"] = not st.session_state["add_30hz"]

# Génération des signaux selon l'état
if st.session_state["add_60hz"]:
    c1 = 0.5 * np.cos(2 * np.pi * 60 * time) * ((time >= 150) & (time <= 250))
else:
    c1 = np.zeros_like(time)

if st.session_state["add_30hz"]:
    c2 = 1 * np.cos(2 * np.pi * 30 * time) * ((time >= 450) & (time <= 500))
else:
    c2 = np.zeros_like(time)

if st.session_state["add_15hz"]:
    c3 = 1.5 * np.cos(2 * np.pi * 15 * time) * ((time >= 400) & (time <= 500))
else:
    c3 = np.zeros_like(time)

if st.session_state["add_5hz"]:
    c4 = 1 * np.cos(2 * np.pi * 5 * time) * ((time >= 0) & (time <= 200))
else:
    c4 = np.zeros_like(time)

#Bouton bruit
if "add_noise" not in st.session_state:
    st.session_state["add_noise"] = False

if st.button("Ajouter du bruit blanc"):
    st.session_state["add_noise"] = not st.session_state["add_noise"]

if st.session_state["add_noise"]:
    noise =  np.random.normal(0, 0.5, size=time.shape)  # Bruit blanc
else:
    noise = np.zeros_like(time)

x = carrier + c1 + c2 + c3 + c4 + noise


f_spec, t_spec, Sxx = sp.signal.spectrogram(x, fs)


# Création du graphique du spectrogramme
fig_spec = go.Figure(data=go.Heatmap(
    z=Sxx,
    x=t_spec,
    y=f_spec,
    colorscale='Turbo',  # plus lisible que 'Viridis' pour ce type de données
    colorbar=dict(title='Puissance '),
    zsmooth='best'
))

fig_spec.update_layout(
    title="Spectrogramme ",
    xaxis=dict(
        title="Temps (s)",
        showgrid=True,
        gridcolor='rgba(200,200,200,0.2)'
    ),
    yaxis=dict(
        title="Fréquence (Hz)",
        range=[0, 100],  # Limiter la bande utile (par ex. 0-20 Hz)
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


# Sélection de l'intervalle de temps à afficher
st.subheader("Choisissez le début de l'intervalle de temps à visualiser")
t_min = st.slider(
    "Début de l'intervalle (en secondes)",
    min_value=float(time[0]),
    max_value=float(time[-1] - 1.5),
    value=float(time[0]),
    step=0.1
)
t_max = t_min + 1.5

# Visualisation
fig = go.Figure()

# Signal temporel (affichage selon l'intervalle choisi)
mask = (time >= t_min) & (time <= t_max)
fig.add_trace(go.Scatter(
    x=time[mask], y=x[mask],
    mode='lines',
    name='Signal',
    line=dict(color='blue', width=1)
))

fig.update_layout(
    title="Signal cosinus à fréquence variable",
    xaxis_title="Temps (s)",
    xaxis_range=[t_min, t_max],
    yaxis_title="Amplitude"
)
st.plotly_chart(fig, use_container_width=True)






# Explications
st.markdown(f"""
## Analyse du spectrogramme

- **Axe horizontal** : Temps (de 0 à {t_spec[-1]} s)
- **Axe vertical** : Fréquence (de {f_spec[0]:.1f} à {f_spec[-1]:.1f} Hz)
- **Couleur** : Intensité du signal (plus c'est chaud, plus c'est intense)

**Observation** :
- On voit clairement que la fréquence monte de 0 Hz à {f_max} Hz
- La trace est nette car le signal est pur (pas de bruit)
""")

st.markdown("""
## Applications réelles
- Analyse de la parole (reconnaissance vocale)
- Étude des chants d'oiseaux
- Diagnostic de machines (vibrations)
""")