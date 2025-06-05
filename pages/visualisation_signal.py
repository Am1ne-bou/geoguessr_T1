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
    La **puissance** d'un signal, c'est une façon de mesurer "combien d'énergie" il transporte en moyenne.
    Pour un signal sinusoïdal, la puissance dépend de l'amplitude : plus l'amplitude est grande, plus la puissance est grande.
    Pour mieux comprendre, on affiche ci-dessous le signal (en bleu) et son carré (en orange) : le carré du signal montre comment la puissance varie au cours du temps.
    Plus la courbe orange est haute, plus le signal est puissant à cet instant.
    """
)

y2 = y**2
fig_puissance = go.Figure()
fig_puissance.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal y(t)', line=dict(color='blue')))
fig_puissance.add_trace(go.Scatter(x=t, y=y2, mode='lines', name='puissance instantanée', line=dict(color='orange')))
fig_puissance.update_layout(
    title="Signal et carré du signal (puissance instantanée)",
    xaxis_title="Temps (t)",
    yaxis_title="Amplitude / Puissance instantanée",
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


x = carrier

f_spec, t_spec, Sxx = sp.signal.spectrogram(x, fs)


# Spectrogramme
plt.figure(figsize=(10, 6))
plt.pcolormesh(t_spec, f_spec, Sxx, shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Intensity (dB)')
st.pyplot(plt.gcf())


# Visualisation
fig = go.Figure()

# Signal temporel
fig.add_trace(go.Scatter(
    x=time, y=x,
    mode='lines',
    name='Signal',
    line=dict(color='blue', width=1)
))

fig.update_layout(
    title="Signal cosinus à fréquence variable",
    xaxis_title="Temps (s)",
    xaxis_range=[0, time[500]],
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