import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


st.title("Visualisation interactive de la fonction $A \cos(2\pi f t + \phi)$")
st.write(
    """
    Un signal est une grandeur physique qui varie en fonction du temps et qui peut transporter de l'information.
    Dans cette application, on visualise un signal sinusoïdal de la forme $A \cos(2\pi f t + \phi)$, où :
    - $A$ est l'amplitude,
    - $f$ la fréquence,
    - $\phi$ la phase.
    Vous pouvez modifier ces paramètres pour observer leur influence sur la forme du signal.
    """
)
A = st.number_input("Amplitude (A)", min_value=0.0, max_value=100000.0, value=1.0, step=10.0)
f = st.number_input("Fréquence (f)", min_value=0.0, max_value=10000000.0, value=1.0, step=1.0)
phi = st.number_input("Phase (φ en radians)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f")

t = np.linspace(0, 2, 1000)
y = A * np.cos(2 * np.pi * f * t + phi)

fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(t, y, label=fr'$A={A},\ f={f},\ \phi={phi:.2f}$')
ax.set_title(r'$A \cos(2\pi f t + \phi)$')
ax.set_xlabel('Temps (t)')
ax.set_ylabel('Amplitude')
ax.grid(True)
ax.legend()

st.pyplot(fig)