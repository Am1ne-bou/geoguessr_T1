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

st.header("2. Spectrogramme de l'onde sismique")
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

    # Signal temporel (affichage selon l'intervalle choisi)
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

    # Affichage dans Streamlit
    st.plotly_chart(fig_spec, use_container_width=True)

