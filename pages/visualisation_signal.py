import numpy as np
import streamlit as st
import plotly.graph_objects as go

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

A = st.slider("Amplitude (A)", min_value=0.0, max_value=100.0, value=50.0, step=1.0)
f = st.slider("Fréquence (f)", min_value=4.0, max_value=15.0, value=1.0, step=0.1)
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