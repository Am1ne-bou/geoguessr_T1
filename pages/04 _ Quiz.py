import streamlit as st


# Configuration de la page
st.set_page_config(
    page_title="Onde sismique",
    layout="wide")



st.title("📊 Quiz : Ondes sismiques ")


# Initialisation des réponses dans session_state si elles n'existent pas
if 'answers' not in st.session_state:
    st.session_state.answers = {}

# Fonction pour gérer les questions
def question(num, question_text, options, correct_answer, explanation):
    st.markdown(f"**{num} {question_text}**")
    key = f"q{num.split('️ ')[0]}"
    
    # Si pas encore répondu, afficher les options sans feedback
    if key not in st.session_state.answers:
        response = st.radio("Choisissez une réponse:", options, key=key)
        if st.button("Valider", key=f"btn_{key}"):
            st.session_state.answers[key] = response
            if response == correct_answer:
                st.success(f"✅ Correct ! {explanation}")
            else:
                st.error(f"❌ {explanation}")
    else:
        # Afficher la question avec le feedback si déjà répondu
        response = st.radio("Choisissez une réponse:", options, key=key, index=options.index(st.session_state.answers[key]))
        if st.session_state.answers[key] == correct_answer:
            st.success(f"✅ Correct ! {explanation}")
        else:
            st.error(f"❌ {explanation}")

# Liste de toutes les questions
questions = [
    {
        "num": "1️⃣",
        "question": "Combien de types d'ondes sismiques principales observe-t-on généralement ?",
        "options": ["2", "3", "4"],
        "correct": "3",
        "explanation": " Il y a les ondes P, S et les ondes de surface."
    },
    {
        "num": "2️⃣",
        "question": "Quel appareil enregistre les ondes sismiques ?",
        "options": ["Oscilloscope", "Sismographe", "Accéléromètre"],
        "correct": "Sismographe",
        "explanation": " Le sismographe enregistre les mouvements du sol."
    },
    {
        "num": "3️⃣",
        "question": "Quelle onde est la plus rapide ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde P",
        "explanation": " Les ondes P (primaires) sont les plus rapides."
    },
    {
        "num": "4️⃣",
        "question": "Quelle onde est la plus lente ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde de surface",
        "explanation": " Les ondes de surface sont les plus lentes."
    },
    {
        "num": "5️⃣",
        "question": "Quelle onde est la plus destructrice ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde de surface",
        "explanation": " Les ondes de surface causent les dégâts les plus importants."
    },
    {
        "num": "6️⃣",
        "question": "Quelle onde est une onde de compression ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde P",
        "explanation": " Les ondes P sont des ondes de compression."
    },
    {
        "num": "7️⃣",
        "question": "Quelle onde est une onde de cisaillement ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde S",
        "explanation": " Les ondes S sont des ondes de cisaillement."
    },
    {
        "num": "8️⃣",
        "question": "Quelle onde peut traverser les liquides ?",
        "options": ["Onde P", "Onde S", "Onde de surface"],
        "correct": "Onde P",
        "explanation": " Les ondes P peuvent traverser les liquides."
    },
    {
        "num": "9️⃣",
        "question": "Quelles sont les fréquences observées dans les ondes P ?",
        "options": ["0.1-1 Hz", "8-12 Hz", "10-100 Hz"],
        "correct": "8-12 Hz",
        "explanation": "Les ondes P ont des fréquences de 8 à 12 Hz."
    },
    {
        "num": "🔟",
        "question": "Quelles sont les fréquences observées dans les ondes S ?",
        "options": ["0.1-1 Hz", "8-12 Hz", "10-100 Hz"],
        "correct": "0.1-1 Hz",
        "explanation": "Les ondes S ont des fréquences de 0.1 à 1 Hz."
    }
]

# Afficher toutes les questions standard
for q in questions:
    question(q["num"], q["question"], q["options"], q["correct"], q["explanation"])

# Question spéciale avec explication physique
st.markdown("1️⃣1️⃣ Comment estimer la distance à l'épicentre du séisme si on a les temps d'arrivée des ondes P et S et on connaît leurs vitesses ?")
q11_options = [
    "D = (Vp - Vs) × (t_s - t_p)",
    "D = (Vp × Vs) / (Vp - Vs) × (t_s - t_p)",
    "D = (Vp + Vs) × (t_s - t_p)"
]
q11_key = "q11"

if q11_key not in st.session_state.answers:
    q11_response = st.radio("Choisissez une réponse:", q11_options, key=q11_key)
    if st.button("Valider la réponse", key="btn_q11"):
        st.session_state.answers[q11_key] = q11_response
        if q11_response == "D = (Vp × Vs) / (Vp - Vs) × (t_s - t_p)":
            st.success("✅ Correct ! La distance à l'épicentre se calcule en fonction des vitesses des ondes et de leur différence de temps d'arrivée.")
        else:
            st.error("❌ Mauvaise réponse.")
else:
    q11_response = st.radio("Choisissez une réponse:", q11_options, key=q11_key, index=q11_options.index(st.session_state.answers[q11_key]))
    if st.session_state.answers[q11_key] == "D = (Vp × Vs) / (Vp - Vs) × (t_s - t_p)":
        st.success("✅ Correct ! La distance à l'épicentre se calcule en fonction des vitesses des ondes et de leur différence de temps d'arrivée.")
    else:
        st.error("❌ Mauvaise réponse.")

# Bouton pour afficher l'explication physique
if st.session_state.answers.get(q11_key) and st.button("Afficher l'explication physique"):
    st.write("""
### Dérivation de la Formule

Pour une distance **D** à l'épicentre:
- Temps onde P: $t_p = \\frac{{D}}{{V_p}}$
- Temps onde S: $t_s = \\frac{{D}}{{V_s}}$
- Différence: $Δt = t_s - t_p = D\\left(\\frac{{1}}{{V_s}} - \\frac{{1}}{{V_p}}\\right)$

En résolvant pour :
$D = \\frac{{Δt}}{{\\frac{{1}}{{V_s}} - \\frac{{1}}{{V_p}}}} = \\frac{{V_p × V_s}}{{V_p - V_s}} × Δt$

Cette formule permet d'estimer la distance à l'épicentre en utilisant les vitesses des ondes P et S et la différence de temps d'arrivée.

""")

