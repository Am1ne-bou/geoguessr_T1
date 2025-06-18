import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="Signal Sonore", layout="wide")

st.title("Enregistrement et analyse d'un signal sonore")

st.header("1. Enregistrez ou importez un son")
st.write(
    """
    Un **son** est une vibration qui se propage dans l'air et que l'on peut entendre avec nos oreilles.
    Ici, tu peux enregistrer un son ou importer un fichier audio pour l'analyser.
    """
)
if "audio" not in st.session_state:
    st.session_state["audio"] = None

col1, col2 = st.columns(2)
with col1:
    audio_recorded = st.audio_input("Clique ici pour enregistrer un son (max 10s)")
    if audio_recorded is not None:
        st.session_state["audio"] = audio_recorded

with col2:
    audio_uploaded = st.file_uploader("Ou importe un audio avec 3 notes différentes (mp3/wav)", type=["mp3", "wav"])
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
    st.write(
        """
        Un **signal sonore** est une courbe qui représente comment le son varie au cours du temps.
        Sur le graphique ci-dessous, l'axe horizontal correspond au temps (en secondes) et l'axe vertical à l'amplitude du son.
        Une grande amplitude correspond à un son fort, une faible amplitude à un son doux.
        """
    )
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal audio'))
    fig.update_layout(
        title="Signal audio enregistré",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig, use_container_width=True, key="signal_time")

    st.header("3. Fréquences du son")
    st.write(
        """
        Un **son** peut être composé de plusieurs notes différentes.
        Chaque note correspond à une **fréquence** : c'est le nombre de vibrations du son par seconde, mesuré en Hertz (Hz).
        Plus la fréquence est élevée, plus le son est aigu ; plus elle est basse, plus le son est grave.
        Le graphique ci-dessous montre quelles fréquences sont présentes dans le son.
        Les pics (les bosses) indiquent les notes jouées.
        """
    )
    N = len(y)
    yf = np.fft.rfft(y)
    xf = np.fft.rfftfreq(N, 1 / samplerate)
    amplitude = np.abs(yf)

    fig_fft = go.Figure()
    fig_fft.add_trace(go.Scatter(x=xf, y=amplitude, mode='lines', name='Spectre'))
    fig_fft.update_layout(
        title="Fréquences présentes dans le son",
        xaxis_title="Fréquence (Hz)",
        yaxis_title="Amplitude",
        xaxis_range=[0, 3000],
        template="plotly_white"
    )
    st.plotly_chart(fig_fft, use_container_width=True, key="signal_fft")

    st.info("Astuce : chaque note correspond à un pic dans le graphique. Utilise le tableau ci-dessous pour faire le lien entre fréquence et note.")

    st.markdown(
        "[Voir le tableau de correspondance notes/fréquences (Hz)](https://i0.wp.com/musicordes.fr/wp-content/uploads/2017/02/frequence-notes-hertz.jpg?resize=1024%2C686&ssl=1)"
    )

    st.header("4. Le spectrogramme : les fréquences au fil du temps")
    st.write(
        """
        Un **spectrogramme** est une image qui montre comment les différentes fréquences changent au cours du temps.
        Cela permet de voir à quel moment chaque note apparaît ou disparaît.
        Sur le spectrogramme, chaque bande horizontale représente une note.
        """
    )

    # Spectrogramme d'exemple
    if "show_cos_spectro" not in st.session_state:
        st.session_state["show_cos_spectro"] = False

    col_cos1, col_cos2 = st.columns([1, 3])
    with col_cos1:
        if st.button(
            "Afficher un exemple de spectrogramme" if not st.session_state["show_cos_spectro"] else "Masquer l'exemple",
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
                    z=Sxx_demo,
                    x=t_spec_demo,
                    y=f_demo,
                    colorscale="Viridis",
                    colorbar=dict(title="dB"),
                )
            )
            fig_demo.update_layout(
                title="Spectrogramme d'un cosinus (500 Hz)",
                xaxis_title="Temps (s)",
                yaxis_title="Fréquence (Hz)",
                yaxis_range=[0, 2000],
                template="plotly_white"
            )
            st.plotly_chart(fig_demo, use_container_width=True)

    st.header("5. À toi de jouer !")
    st.write("""
        Dans ce fichier audio, il y a 3 notes différentes jouées les unes après les autres.

        Regarde le graphique des fréquences et le tableau pour deviner quelles sont les 3 notes présentes.

         ⚠️ **Remarque importante :**  
        Quand tu joues une note (ou que tu parles), il n'y a pas qu'une seule fréquence dans le son !  
        En plus de la fréquence principale (appelée **fréquence fondamentale**), il y a souvent d'autres fréquences plus hautes, appelées **harmoniques**.  
        Ces harmoniques sont des multiples de la fréquence principale et donnent la "couleur" ou le "timbre" du son.  
        C'est pour cela que, sur le spectrogramme, tu peux voir plusieurs bandes en même temps : la plus basse correspond à la note jouée, les autres sont ses harmoniques.
    """)

    st.write(
        "Pour voir à quel moment chaque note commence, clique sur le bouton ci-dessous pour afficher le **spectrogramme** :"
    )

    if st.button("Afficher le spectrogramme du son"):
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
            title="Spectrogramme du son",
            xaxis_title="Temps (s)",
            yaxis_title="Fréquence (Hz)",
            yaxis_range=[0, 3000],
            template="plotly_white"
        )
        st.plotly_chart(fig_spec, use_container_width=True, key="spectrogramme")
        st.info("Sur le spectrogramme, chaque note apparaît comme une bande horizontale à une certaine hauteur. Repère à quel moment chaque note commence et finit.")

    st.header("6. Compare deux voix sur le même mot")
    st.write(
        """
        Chaque personne a une voix différente.
        La **fréquence dominante** d'une voix correspond à la hauteur principale du son : une voix grave a une fréquence basse, une voix aiguë a une fréquence haute.
        Enregistre ou importe deux personnes disant le même mot, puis compare la fréquence dominante de chaque voix.
        """
    )

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Voix 1")
        audio1 = st.audio_input("Enregistre ou importe la voix 1", key="audio1")
    with col4:
        st.subheader("Voix 2")
        audio2 = st.audio_input("Enregistre ou importe la voix 2", key="audio2")

    if audio1 is not None and audio2 is not None:
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

        st.write(f"**Fréquence dominante voix 1 : {freq_dom1:.1f} Hz**")
        st.write(f"**Fréquence dominante voix 2 : {freq_dom2:.1f} Hz**")

        if abs(freq_dom1 - freq_dom2) < 10:
            st.success("Les deux voix ont une fréquence dominante très proche !")
        else:
            st.info("Les fréquences dominantes sont différentes, ce qui reflète la différence de hauteur de voix.")

        col5, col6 = st.columns(2)
        with col5:
            fig1 = go.Figure()
            fig1.add_trace(go.Scatter(x=xf1, y=amplitude1, mode='lines', name='Spectre voix 1'))
            fig1.update_layout(
                title="Fréquences de la voix 1",
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
                title="Fréquences de la voix 2",
                xaxis_title="Fréquence (Hz)",
                yaxis_title="Amplitude",
                xaxis_range=[0, 3000],
                template="plotly_white"
            )
            st.plotly_chart(fig2, use_container_width=True, key="fft_voix2")
    else:
        st.info("Enregistre ou importe deux voix pour comparer leurs fréquences dominantes.")

else:
    st.info("Enregistre ou importe un son avec 3 notes différentes pour commencer l'activité.")
