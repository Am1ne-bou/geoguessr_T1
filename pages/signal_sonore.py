import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.title("Enregistrement et analyse d'un signal sonore")

st.header("1. Enregistrez votre voix ou un son")
audio = st.audio_input("Cliquez pour enregistrer un son (max 10s)")

if audio is not None:
    import soundfile as sf #voir biblio soundfile en detail pour mieux savoir comment ça fonctionne
    import io # entrée/sortie deflux pratique pour manipuler fichiers audio

    data, samplerate = sf.read(io.BytesIO(audio.getvalue())) 
    y = data[:, 0] if data.ndim > 1 else data #probleme avec stereo (+ facile d'utiliser un seul canal)
    t = np.arange(len(y)) / samplerate

    st.audio(audio, format="audio/wav")
    st.header("2. Visualisation du signal dans le temps")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal audio'))
    fig.update_layout(
        title="Signal audio enregistré",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True)

    st.header("3. Spectre de fréquences")
    N = len(y)
    yf = np.fft.rfft(y)
    xf = np.fft.rfftfreq(N, 1 / samplerate)
    amplitude = np.abs(yf)

    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=xf, y=amplitude, mode='lines', name='Spectre'))
    fig_fft.update_layout(
        title="Spectre du signal audio",
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Amplitude",
        xaxis_range=[0, 2000],  # Limite l'affichage du spectre de 0 à 3000 Hz
        template="plotly_white"
    )
    st.plotly_chart(fig_fft, use_container_width=True)

    st.info("Astuce : le pic principal du spectre correspond à la fréquence dominante du son enregistré.")

    freq_dominante = xf[np.argmax(amplitude)]
    st.subheader("4. Quelle est la fréquence dominante ?")
    if st.button("Afficher la fréquence dominante"):
        st.success(f"La fréquence dominante est : {freq_dominante:.1f} Hz")
    else:
        st.info("Essayez de deviner la fréquence dominante avant de cliquer !")

    # --- Quiz rapide ---
    st.subheader("5. Quiz rapide")
    question = st.radio(
        "Si vous sifflez une note aiguë, que se passe-t-il sur le spectre ?",
        [
            "Le pic principal se déplace vers la droite (fréquences hautes)",
            "Le pic principal se déplace vers la gauche (fréquences basses)",
            "Le spectre ne change pas"
        ]
    )
    if st.button("Vérifier ma réponse"):
        if question == "Le pic principal se déplace vers la droite (fréquences hautes)":
            st.success("Bravo ! C’est la bonne réponse.")
        else:
            st.error("Ce n'est pas la bonne réponse. Essayez encore !")

else:
    st.info("Enregistrez un son pour voir son signal et son spectre.")


