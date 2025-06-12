import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Signal Sonore", layout="wide")

st.title("Enregistrement et analyse d'un signal sonore")

st.header("1. Enregistrez ou importez un son")
if "audio" not in st.session_state:
    st.session_state["audio"] = None

col1, col2 = st.columns(2)
with col1:
    audio_recorded = st.audio_input("Cliquez pour enregistrer un son (max 10s)")
    if audio_recorded is not None:
        st.session_state["audio"] = audio_recorded

with col2:
    audio_uploaded = st.file_uploader("Upload un audio avec 3 notes différentes successives (mp3/wav)", type=["mp3", "wav"])
    if audio_uploaded is not None:
        st.session_state["audio"] = audio_uploaded

audio = st.session_state["audio"]

if audio is not None:
    import soundfile as sf
    import io

    data, samplerate = sf.read(io.BytesIO(audio.getvalue()))
    y = data[:, 0] if data.ndim > 1 else data
    t = np.arange(len(y)) / samplerate

    st.audio(audio, format="audio/mp3" if hasattr(audio, "type") and audio.type == "audio/mp3" else "audio/wav")

    st.header("2. Visualisation du signal dans le temps")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal audio'))
    fig.update_layout(
        title="Signal audio enregistré",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True, key="signal_time")

    st.header("3. Spectre de fréquences global")
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
        xaxis_range=[0, 3000],
        template="plotly_white"
    )
    st.plotly_chart(fig_fft, use_container_width=True, key="signal_fft")

    st.info("Astuce : chaque note correspond à un pic dans le spectre. Utilise le tableau ci-dessous pour faire le lien entre fréquence et note.")

    st.markdown(
        "[Voir le tableau de correspondance notes/fréquences (Hz)](https://i0.wp.com/musicordes.fr/wp-content/uploads/2017/02/frequence-notes-hertz.jpg?resize=1024%2C686&ssl=1)"
    )

    st.header("Principe du spectrogramme")
    st.write(
        """
        Un **spectrogramme** permet de visualiser comment les fréquences d'un signal évoluent au cours du temps.
        Contrairement au spectre global qui donne toutes les fréquences présentes dans le signal, le spectrogramme montre à quel moment chaque fréquence apparaît ou disparaît.
        Voici un exemple de spectrogramme pour un signal simple : un cosinus de fréquence 500 Hz.
        """
    )

    # Utilisation de session_state pour afficher/masquer le spectrogramme du cosinus
    if "show_cos_spectro" not in st.session_state:
        st.session_state["show_cos_spectro"] = False

    col_cos1, col_cos2 = st.columns([1, 3])
    with col_cos1:
        if st.button(
            "Afficher le spectrogramme du cosinus" if not st.session_state["show_cos_spectro"] else "Masquer le spectrogramme du cosinus",
            key="toggle_cos_spectro"
        ):
            st.session_state["show_cos_spectro"] = not st.session_state["show_cos_spectro"]

    with col_cos2:
        if st.session_state["show_cos_spectro"]:
            from scipy.signal import spectrogram
            fs_demo = 8000
            t_demo = np.linspace(0, 1, fs_demo, endpoint=False)
            y_demo = np.cos(2 * np.pi * 500 * t_demo)
            f_demo, t_spec_demo, Sxx_demo = spectrogram(y_demo, fs=fs_demo, nperseg=512, noverlap=256)
            fig_demo = go.Figure(
                data=go.Heatmap(
                    z=10 * np.log10(Sxx_demo + 1e-10),
                    x=t_spec_demo,
                    y=f_demo,
                    colorscale="Viridis",
                    colorbar=dict(title="dB"),
                )
            )
            fig_demo.update_layout(
                title="Spectrogramme d'un cosinus de 500 Hz",
                xaxis_title="Temps (s)",
                yaxis_title="Fréquence (Hz)",
                yaxis_range=[0, 2000],
                template="plotly_white"
            )
            st.plotly_chart(fig_demo, use_container_width=True)

    st.header("4. À vous de jouer !")
    st.write(
        "Dans ce fichier audio, il y a 3 notes différentes jouées successivement. "
        "À l'aide du spectre ci-dessus et du tableau, essayez de trouver quelles sont les 3 notes présentes et leur fréquence."
    )

    st.write(
        "Pour savoir à quel moment chaque note arrive, clique sur le bouton ci-dessous pour afficher le **spectrogramme** (fréquence en fonction du temps) :"
    )

    if st.button("Afficher le spectrogramme"):
        from scipy.signal import spectrogram

        f, t_spec, Sxx = spectrogram(y, fs=samplerate, nperseg=2048, noverlap=1024)
        fig_spec = go.Figure(
            data=go.Heatmap(
                z=10 * np.log10(Sxx + 1e-10),
                x=t_spec,
                y=f,
                colorscale="Viridis",
                colorbar=dict(title="dB"),
            )
        )
        fig_spec.update_layout(
            title="Spectrogramme du signal audio",
            xaxis_title="Temps (s)",
            yaxis_title="Fréquence (Hz)",
            yaxis_range=[0, 3000],
            template="plotly_white"
        )
        st.plotly_chart(fig_spec, use_container_width=True, key="spectrogramme")
        st.info("Sur le spectrogramme, chaque note apparaît comme une bande horizontale à une fréquence donnée. Repère à quel moment chaque note commence et finit.")
        # --- Section 5 : Comparer deux voix sur le même mot ---
    st.header("5. Comparez deux voix sur le même mot")
    st.write(
        """
        Enregistrez ou importez deux extraits où deux personnes différentes disent le même mot (par exemple "bonjour").
        Comparez la fréquence dominante de chaque voix pour voir si elles sont différentes.
        """
    )

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Voix 1")
        audio1 = st.audio_input("Enregistrez ou importez la voix 1", key="audio1")
    with col4:
        st.subheader("Voix 2")
        audio2 = st.audio_input("Enregistrez ou importez la voix 2", key="audio2")

    if audio1 is not None and audio2 is not None:
        import soundfile as sf
        import io

        # Analyse voix 1
        data1, sr1 = sf.read(io.BytesIO(audio1.getvalue()))
        y1 = data1[:, 0] if data1.ndim > 1 else data1
        N1 = len(y1)
        yf1 = np.fft.rfft(y1)
        xf1 = np.fft.rfftfreq(N1, 1 / sr1)
        amplitude1 = np.abs(yf1)
        freq_dom1 = xf1[np.argmax(amplitude1)]

        # Analyse voix 2
        data2, sr2 = sf.read(io.BytesIO(audio2.getvalue()))
        y2 = data2[:, 0] if data2.ndim > 1 else data2
        N2 = len(y2)
        yf2 = np.fft.rfft(y2)
        xf2 = np.fft.rfftfreq(N2, 1 / sr2)
        amplitude2 = np.abs(yf2)
        freq_dom2 = xf2[np.argmax(amplitude2)]

        # Affichage résultats
        st.write(f"**Fréquence dominante voix 1 : {freq_dom1:.1f} Hz**")
        st.write(f"**Fréquence dominante voix 2 : {freq_dom2:.1f} Hz**")

        if abs(freq_dom1 - freq_dom2) < 10:
            st.success("Les deux voix ont une fréquence dominante très proche !")
        else:
            st.info("Les fréquences dominantes sont différentes, ce qui reflète la différence de hauteur de voix.")

        # Affichage des spectres côte à côte
        col5, col6 = st.columns(2)
        with col5:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=xf1, y=amplitude1, mode='lines', name='Spectre voix 1'))
            fig1.update_layout(
                title="Spectre voix 1",
                xaxis_title="Fréquence (Hz)",
                yaxis_title="Amplitude",
                xaxis_range=[0, 3000],
                template="plotly_white"
            )
            st.plotly_chart(fig1, use_container_width=True, key="fft_voix1")
        with col6:
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=xf2, y=amplitude2, mode='lines', name='Spectre voix 2'))
            fig2.update_layout(
                title="Spectre voix 2",
                xaxis_title="Fréquence (Hz)",
                yaxis_title="Amplitude",
                xaxis_range=[0, 3000],
                template="plotly_white"
            )
            st.plotly_chart(fig2, use_container_width=True, key="fft_voix2")
    else:
        st.info("Enregistrez ou importez deux voix pour comparer leurs fréquences dominantes.")


else:
    st.info("Enregistrez ou importez un son avec 3 notes différentes pour commencer l'activité.")


