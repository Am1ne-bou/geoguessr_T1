import numpy as np
import plotly.graph_objects as go
import streamlit as st

# Configuration de la page
st.set_page_config(
    page_title="Capteurs et Échantillonnage",
    page_icon="🎤",
    layout="wide"
)

st.title("🎤 Capteurs et Échantillonnage d'un Signal")

st.header("1. Qu'est-ce qu'un capteur ?")
st.write("""
Un **capteur** transforme une grandeur physique (température, lumière, son, pression, etc.) en un signal électrique exploitable par un ordinateur ou un appareil électronique.

**Exemples de capteurs courants** :
- Microphone (son)
- Thermomètre électronique (température)
- Capteur de pression (pression atmosphérique)
- Cellule photovoltaïque (lumière)
- Accéléromètre (mouvement)
- Capteur de CO₂ (qualité de l'air)
""")

st.image("https://anatole-france.ecollege.haute-garonne.fr/lectureFichiergw.do?ID_FICHIER=1518729882243", caption="Quelques exemples de capteurs utilisés en sciences et technologie", use_container_width=True)

st.markdown("**Quiz rapide :**")
q1 = st.radio(
    "Quel capteur permet de mesurer la qualité de l'air dans une salle de classe ?",
    ["Thermomètre", "Capteur de CO₂", "Microphone", "Capteur UV"],
    key="q1"
)
if st.checkbox("Afficher la réponse (quiz rapide)", key="show_quick_quiz"):
    if q1:
        if q1 == "Capteur de CO₂":
            st.success("Bonne réponse !")
        else:
            st.warning("Ce n'est pas le bon capteur. Essaie encore !")

st.info("Les capteurs modernes sont souvent petits, précis, abordables et faciles à connecter à des ordinateurs ou microcontrôleurs (Arduino, micro:bit, etc.).")

st.header("2. L'échantillonnage : transformer un signal continu en signal numérique")
st.write("""
L'**échantillonnage** consiste à prélever régulièrement des valeurs d'un signal continu (comme le son ou la température) pour le transformer en une suite de nombres utilisables par un ordinateur.

- La **fréquence d'échantillonnage** (fs) est le nombre de mesures par seconde (en Hz).
- Plus fs est élevée, plus le signal numérique ressemble au signal original.
- Si fs est trop basse, on perd des informations et le signal est déformé (aliasing).

**Exemple** : Pour la voix humaine, on utilise souvent 8 000 Hz ; pour la musique, 44 100 Hz (CD audio).

**Le théorème de Shannon** (ou Shannon-Nyquist) dit que pour bien enregistrer un signal, il faut que la fréquence d'échantillonnage soit **au moins deux fois plus grande** que la fréquence la plus élevée présente dans le signal.  
Sinon, certaines fréquences ne seront pas bien enregistrées et le signal sera déformé.
""")

st.markdown("**Quiz :**")
q2 = st.radio(
    "Si tu veux enregistrer un son contenant des fréquences jusqu'à 10 000 Hz, quelle doit être la fréquence d'échantillonnage minimale ?",
    ["5 000 Hz", "10 000 Hz", "20 000 Hz", "40 000 Hz"],
    key="q2"
)
if st.checkbox("Afficher la réponse (quiz échantillonnage)", key="show_quiz_ech"):
    if q2:
        if q2 == "20 000 Hz":
            st.success("Bravo ! Selon le théorème de Shannon, il faut au moins deux fois la fréquence maximale.")
        else:
            st.warning("Ce n'est pas la bonne réponse. Cherche la règle du double !")

st.header("3. Visualisation interactive : compose ton propre signal sonore")
st.write("""
Compose un signal en additionnant plusieurs ondes cosinus de fréquences et d'amplitudes différentes, puis observe l'effet de l'échantillonnage.
""")

col1, col2, col3, col4 = st.columns(4)
signals = []
with col1:
    st.header("Composante 1")
    A1 = st.number_input("Amplitude (A1)", min_value=0.0, value=1.0, step=0.1, key="A1")
    f1 = st.number_input("Fréquence (f1)", min_value=0.0, value=10.0, step=0.1, key="f1")
    phi1 = st.number_input("Phase (φ1)", min_value=0.0, max_value=float(2*np.pi), value=0.0, step=0.1, format="%.2f", key="phi1")
    signals.append({"A": A1, "f": f1, "phi": phi1})
with col2:
    st.header("Composante 2")
    A2 = st.number_input("Amplitude (A2)", min_value=0.0, value=0.8, step=0.1, key="A2")
    f2 = st.number_input("Fréquence (f2)", min_value=0.0, value=30.0, step=0.1, key="f2")
    phi2 = st.number_input("Phase (φ2)", min_value=0.0, max_value=float(2*np.pi), value=np.pi/2, step=0.1, format="%.2f", key="phi2")
    signals.append({"A": A2, "f": f2, "phi": phi2})
with col3:
    st.header("Composante 3")
    A3 = st.number_input("Amplitude (A3)", min_value=0.0, value=0.6, step=0.1, key="A3")
    f3 = st.number_input("Fréquence (f3)", min_value=0.0, value=50.0, step=0.1, key="f3")
    phi3 = st.number_input("Phase (φ3)", min_value=0.0, max_value=float(2*np.pi), value=np.pi, step=0.1, format="%.2f", key="phi3")
    signals.append({"A": A3, "f": f3, "phi": phi3})
with col4:
    st.header("Composante 4")
    A4 = st.number_input("Amplitude (A4)", min_value=0.0, value=0.4, step=0.1, key="A4")
    f4 = st.number_input("Fréquence (f4)", min_value=0.0, value=70.0, step=0.1, key="f4")
    phi4 = st.number_input("Phase (φ4)", min_value=0.0, max_value=float(2*np.pi), value=3*np.pi/2, step=0.1, format="%.2f", key="phi4")
    signals.append({"A": A4, "f": f4, "phi": phi4})

t = np.linspace(0, 1, 1000)
signal_final = np.zeros_like(t)
individual_signals = []
for sig in signals:
    component = sig["A"] * np.cos(2 * np.pi * sig["f"] * t + sig["phi"])
    signal_final += component
    individual_signals.append(component)

st.latex(r"f(t) = " + " + ".join([f"A{i} \cos(2 \pi f{i} t + φ{i})" for i in range(1, 5)]))

tab1, tab2 = st.tabs(["Signal resultant", "Composantes Individuelles"])
with tab1:
    st.header("Signal Resultant")
    st.plotly_chart(go.Figure(data=go.Scatter(x=t, y=signal_final, mode='lines', name='Signal Resultant')), use_container_width=True)
with tab2:
    st.header("Composantes Individuelles")
    fig_individual = go.Figure()
    for i, component in enumerate(individual_signals, start=0):
        fig_individual.add_trace(go.Scatter(x=t, y=component, mode='lines', name=f'Composante {i+1}'))    
    st.plotly_chart(fig_individual, use_container_width=True)

fs = st.slider("Fréquence d'échantillonnage (fs)", 0, 1000, 200, step=10, key="fs")
y_continu = signal_final
t_sampled = np.arange(0, 1, 1/fs)
y_sampled = np.zeros_like(t_sampled)
for sig in signals:
    component_sampled = sig["A"] * np.cos(2 * np.pi * sig["f"] * t_sampled + sig["phi"])
    y_sampled += component_sampled

fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y_continu, mode='lines', name='Signal Continu', line=dict(color='blue')))
max_points = 200
if len(t_sampled) > max_points:
    indices = np.linspace(0, len(t_sampled) - 1, max_points, dtype=int)
    t_sampled_plot = t_sampled[indices]
    y_sampled_plot = y_sampled[indices]
else:
    t_sampled_plot = t_sampled
    y_sampled_plot = y_sampled
fig.add_trace(go.Scatter(x=t_sampled_plot, y=y_sampled_plot, mode='markers', name='Signal Échantillonné', marker=dict(color='red', size=4)))
fig.update_layout(
    title="Échantillonnage d'un Signal cosusoïdal",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    legend_title="Légende",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

yf = np.fft.rfft(y_sampled)
xf = np.fft.rfftfreq(len(y_sampled), 1 / fs)
amplitude = np.abs(yf)
seuil = 0.05 * np.max(amplitude)
freq_presentes = xf[amplitude > seuil]
if len(freq_presentes) > 0:
    freq_plus_haute = np.max(freq_presentes)
else:
    st.info("Aucune fréquence significative détectée dans le signal échantillonné.")

st.write("""
**À retenir :**
- Si la fréquence d'échantillonnage est trop basse, le signal échantillonné ne ressemble plus au signal original (aliasing ou repliement spectral).
- Pour bien échantillonner un signal, il faut que la fréquence d'échantillonnage soit au moins deux fois plus grande que la fréquence la plus élevée du signal (théorème de Shannon/Nyquist).
""")

st.header("4. Le théorème de Shannon (ou Shannon-Nyquist)")
st.write("""
Le **théorème de Shannon** dit :  
> Pour pouvoir reconstituer correctement un signal, il faut que la fréquence d'échantillonnage soit **au moins deux fois supérieure** à la fréquence maximale présente dans le signal.

**Exemple :**  
- Pour enregistrer un son contenant des fréquences jusqu'à 20 000 Hz (oreille humaine), il faut échantillonner à au moins 40 000 Hz.
- C'est pourquoi les CD audio utilisent 44 100 Hz.

Si on ne respecte pas ce théorème, on observe des artefacts appelés **aliasing** : des sons parasites ou des signaux déformés.
""")

st.header("5. Expérimente avec ta propre voix ou un son réel !")
st.write("""
Enregistre un son avec le micro ci-dessous **ou importe un fichier audio**. Tu pourras ensuite choisir différentes fréquences d'échantillonnage pour voir et entendre la différence.
""")

col_audio1, col_audio2 = st.columns(2)
with col_audio1:
    audio_input = st.audio_input("Enregistre un son (max 10s)", key="audio_input")
with col_audio2:
    audio_uploaded = st.file_uploader("Ou importe un fichier audio (wav, mp3)", type=["wav", "mp3"], key="audio_uploaded")
audio = audio_input if audio_input is not None else audio_uploaded

if audio is not None:
    import soundfile as sf
    import io

    data, samplerate = sf.read(io.BytesIO(audio.getvalue()))
    y = data[:, 0] if data.ndim > 1 else data
    t = np.arange(len(y)) / samplerate

    st.audio(audio, format="audio/wav")

    st.subheader("Visualisation du signal enregistré")
    fig_audio = go.Figure()
    fig_audio.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal audio'))
    fig_audio.update_layout(
        title="Signal audio enregistré",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude",
        template="plotly_white"
    )
    st.plotly_chart(fig_audio, use_container_width=True, key="audio_time")

    st.subheader("Échantillonne ton signal à une fréquence plus basse")
    fs_user = st.slider("Choisis une fréquence d'échantillonnage (Hz)", 3000, int(samplerate), 4000, step=500)
    t_ech_user = np.arange(0, len(y)/samplerate, 1/fs_user)
    y_ech_user = np.interp(t_ech_user, t, y)
    max_points = 2000
    if len(t_ech_user) > max_points:
        indices = np.linspace(0, len(t_ech_user) - 1, max_points, dtype=int)
        t_ech_plot = t_ech_user[indices]
        y_ech_plot = y_ech_user[indices]
    else:
        t_ech_plot = t_ech_user
        y_ech_plot = y_ech_user

    fig_ech = go.Figure()
    fig_ech.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Signal original', line=dict(color='blue')))
    fig_ech.add_trace(go.Scatter(x=t_ech_plot, y=y_ech_plot, mode='markers', name='Échantillons', marker=dict(color='red', size=6)))
    fig_ech.update_layout(
        title="Échantillonnage du signal audio",
        xaxis_title="Temps (s)",
        yaxis_title="Amplitude"
    )
    st.plotly_chart(fig_ech, use_container_width=True, key="audio_ech")

    yf = np.fft.fftshift(np.fft.fft(y))
    xf = np.fft.fftshift(np.fft.fftfreq(len(y), 1 / samplerate))
    amplitude = np.abs(yf)
    seuil = 0.05 * np.max(amplitude)
    freq_presentes = np.abs(xf[amplitude > seuil])
    if len(freq_presentes) > 0:
        freq_plus_haute = np.max(freq_presentes)
        st.info(f"La fréquence la plus haute mesurée dans ton signal enregistré (FFT) est : **{freq_plus_haute:.1f} Hz**")
    else:
        freq_plus_haute = 0
        st.info("Aucune fréquence significative détectée dans le signal enregistré.")

    if fs_user < 2 * freq_plus_haute and freq_plus_haute > 0:
        st.warning(
            f"La fréquence d'échantillonnage ({fs_user} Hz) est inférieure à deux fois la fréquence la plus haute présente ({freq_plus_haute:.1f} Hz). "
            "Le son sera très déformé à cause de l'aliasing (théorème de Shannon) !"
        )

    st.write("**À écouter :** Voici le son ré-échantillonné à la fréquence choisie :")
    import soundfile as sf
    import io
    buf = io.BytesIO()
    sf.write(buf, y_ech_user, fs_user, format='WAV')
    st.audio(buf.getvalue(), format="audio/wav")

    st.write("""
    **Question :** Que remarques-tu si tu choisis une fréquence d'échantillonnage trop basse par rapport au son original ?
    """)
    if st.checkbox("Afficher la réponse (audio)"):
        st.info("Le son devient déformé, grave ou méconnaissable. C'est l'effet d'aliasing : on ne peut plus distinguer la vraie fréquence du son.")

st.header("6. Capteurs et échantillonnage dans d'autres domaines")
st.write("""
L'échantillonnage ne sert pas qu'au son ! Il est utilisé pour :
- Les **images numériques** (pixels = échantillons d'intensité lumineuse)
- Les mesures météo (température, pression, humidité, pollution)
- Les signaux biologiques (électrocardiogramme, électroencéphalogramme)
- Les capteurs de pollution (particules fines, CO₂, COV, etc.)

**Quiz :**  
À ton avis, que se passe-t-il si on diminue trop la résolution d'une image numérique ?
""")
q_img = st.radio(
    "Effet d'un sous-échantillonnage sur une image :",
    ["Elle devient floue et perd des détails", "Elle devient plus colorée", "Elle devient plus grande"],
    key="q_img"
)
if st.checkbox("Afficher la réponse (quiz image)", key="show_quiz_img"):
    if q_img:
        if q_img == "Elle devient floue et perd des détails":
            st.success("Exact ! On perd les détails fins de l'image.")
        else:
            st.warning("Ce n'est pas la bonne réponse.")

st.header("7. Grand quiz final : Capteurs & échantillonnage")
st.write("Testez vos connaissances sur tout ce que vous venez d'apprendre !")

score = 0
with st.expander("Question 1"):
    q = st.radio("Un capteur de température mesure :", ["la lumière", "la chaleur", "le son"], key="qf1")
    if q == "la chaleur":
        score += 1
    if st.checkbox("Afficher la réponse (Q1)", key="show_qf1"):
        if q == "la chaleur":
            st.success("Bonne réponse !")
            score += 1
        elif q:
            st.warning("Ce n'est pas la bonne réponse.")

with st.expander("Question 2"):
    q = st.radio("L'échantillonnage consiste à :", [
        "Prendre des mesures à intervalles réguliers",
        "Ajouter du bruit au signal",
        "Augmenter la température du capteur"
    ], key="qf2")
    if q == "Prendre des mesures à intervalles réguliers":
        score += 1
    if st.checkbox("Afficher la réponse (Q2)", key="show_qf2"):
        if q == "Prendre des mesures à intervalles réguliers":
            st.success("Bonne réponse !")
            score += 1
        elif q:
            st.warning("Ce n'est pas la bonne réponse.")

with st.expander("Question 3"):
    q = st.radio("Si la fréquence d'échantillonnage est trop basse, on observe :", [
        "Un signal fidèle",
        "De l'aliasing",
        "Un son plus aigu"
    ], key="qf3")
    if q == "De l'aliasing":
        score += 1
    if st.checkbox("Afficher la réponse (Q3)", key="show_qf3"):
        if q == "De l'aliasing":
            st.success("Bonne réponse !")
            score += 1
        elif q:
            st.warning("Ce n'est pas la bonne réponse.")

with st.expander("Question 4"):
    q = st.radio("Pour bien numériser un signal contenant des fréquences jusqu'à 100 Hz, il faut échantillonner à au moins :", [
        "50 Hz", "100 Hz", "200 Hz", "500 Hz"
    ], key="qf4")
    if q == "200 Hz":
        score += 1
    if st.checkbox("Afficher la réponse (Q4)", key="show_qf4"):
        if q == "200 Hz":
            st.success("Bonne réponse !")
            score += 1
        elif q:
            st.warning("Ce n'est pas la bonne réponse.")

with st.expander("Question 5"):
    q = st.radio("Un pixel dans une image numérique représente :", [
        "Un échantillon de couleur ou de luminosité", "Un capteur de température", "Un son"
    ], key="qf5")
    if q == "Un échantillon de couleur ou de luminosité":
        score += 1
    if st.checkbox("Afficher la réponse (Q5)", key="show_qf5"):
        if q == "Un échantillon de couleur ou de luminosité":
            st.success("Bonne réponse !")
        elif q:
            st.warning("Ce n'est pas la bonne réponse.")

if st.button("Voir mon score au quiz final !"):
    st.info(f"Score : {score}/5")
    if score == 5:
        st.balloons()
        st.success("Félicitations, tu maîtrises les bases des capteurs et de l'échantillonnage !")

st.markdown("---")
st.info("L'échantillonnage est partout autour de nous : son, image, météo, pollution, santé… Les capteurs et le traitement du signal sont au cœur des sciences et des technologies du quotidien !")
