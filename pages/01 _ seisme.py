import streamlit as st
import numpy as np

st.title("Découverte des séismes")
st.video("https://www.youtube.com/watch?v=kU-Q0vFJK_M&ab_channel=LeHuffPost")
st.header("1. Qu'est-ce qu'un séisme ?")
st.write("""
Un **séisme** (ou tremblement de terre) est une vibration du sol causée par la libération soudaine d'énergie dans la croûte terrestre.
Cette énergie se propage sous forme d'ondes sismiques. Les séismes peuvent être provoqués par :
- Le déplacement des plaques tectoniques
- L'activité volcanique
- L'effondrement de cavités souterraines
- L'activité humaine (explosions, mines...)

La plupart des séismes naturels sont dus à la rupture brutale de roches le long d'une faille.
""")

st.markdown("**Question :** À ton avis, où a-t-on le plus de séismes sur Terre ?")
if st.checkbox("Afficher la réponse (zones à risque)"):
    st.info("Les séismes sont plus fréquents près des frontières de plaques tectoniques, comme autour du Pacifique (ceinture de feu), en Méditerranée, ou en Asie du Sud.")

st.header("2. Les ondes sismiques")
st.write("""
Quand un séisme se produit, il génère plusieurs types d'ondes:
- **Ondes P** (premières, de compression): se propagent le plus vite, traversent solides et liquides.
- **Ondes S** (secondaires, de cisaillement): plus lentes, ne traversent que les solides.
- **Ondes de surface**: se propagent à la surface, plus lentes mais souvent les plus destructrices.

Les stations sismiques enregistrent ces ondes sous forme de **signaux**.
""")

st.subheader("Activité 1: Classe les ondes par ordre d'arrivée")
ordre = st.multiselect(
    "Classe ces ondes de la première à la dernière à arriver lors d'un séisme:",
    ["Ondes S", "Ondes de surface", "Ondes P"]
)
if ordre:
    if ordre == ["Ondes P", "Ondes S", "Ondes de surface"]:
        st.success("Bravo ! C'est le bon ordre d'arrivée.")
    else:
        st.warning("Essaie encore. Rappelle-toi : P (premières), S (secondes), puis les ondes de surface.")

st.markdown("**Question :** Pourquoi les ondes S ne traversent-elles pas le noyau externe de la Terre ?")
if st.checkbox("Afficher la réponse (ondes S)"):
    st.info("Parce que le noyau externe est liquide, et les ondes S ne se propagent que dans les solides.")

st.header("3. Un séisme, c'est où et quand ?")
         
st.image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQefF0dub_B01O-md5KDb2fRPlKsIWchzCUHw&s", caption="Schéma d'un séisme")
st.write("""
Quand un séisme a lieu, les ondes partent du foyer et se propagent dans toutes les directions.
""")

st.subheader("Activité 2: Associe les définitions")
options = {
    "Foyer": "Point de départ du séisme en profondeur",
    "Épicentre": "Point à la surface juste au-dessus du foyer",
    "Faille": "Cassure dans la croûte terrestre où se produit le séisme"
}
reponses = {}
for mot in options:
    reponses[mot] = st.selectbox(f"{mot} :", list(options.values()), key=mot)
if st.button("Vérifier mes réponses"):
    score = sum(reponses[mot] == options[mot] for mot in options)
    if score == len(options):
        st.success("Bravo, toutes les définitions sont correctes !")
    else:
        st.warning(f"{score}/{len(options)} bonnes réponses. Essaie encore !")

st.header("4. Mesurer un séisme")
st.write("""
Les séismes sont mesurés par :
- **Magnitude** (échelle de Richter ou de moment) : mesure l'énergie libérée.
- **Intensité** (échelle de Mercalli) : mesure les effets et dégâts observés.

Un séisme de magnitude 6 libère 32 fois plus d'énergie qu'un séisme de magnitude 5 !
""")
st.image("https://static1.assistancescolaire.com/col/images/a0410_00004i03z.jpg")

st.subheader("Activité 3: Vrai ou faux ?")
q1 = st.radio("Un séisme de magnitude 7 est 10 fois plus puissant qu'un séisme de magnitude 6.", ["Vrai", "Faux"], key="q1")
q2 = st.radio("L'intensité d'un séisme dépend de la distance à l'épicentre.", ["Vrai", "Faux"], key="q2")

if st.button("Valider mes réponses (activité 3)"):
    # Correction question 1
    if q1 == "Faux":
        st.success("Bonne réponse pour la question 1 ! Il est environ 32 fois plus puissant.")
    else:
        st.error("Non pour la question 1, il est environ 32 fois plus puissant.")
    # Correction question 2
    if q2 == "Vrai":
        st.success("Exact pour la question 2 ! Plus on est loin, moins on ressent le séisme.")
    else:
        st.error("Faux pour la question 2, l'intensité diminue avec la distance.")

st.header("5. Séisme et signaux: le lien")
st.write("""
Les stations sismiques transforment les vibrations du sol en **signaux** (courbes d'amplitude en fonction du temps).
Ces signaux sont appelés **sismogrammes**.

Un sismogramme est l'enregistrement des mouvements du sol lors d'un séisme, réalisé par un capteur appelé **sismomètre**.
On peut y repérer l'arrivée des différentes ondes (P, S, de surface).

Ci-dessous, un exemple de sismogramme enregistré sur trois axes (vertical, nord-sud, est-ouest) :
""")

st.image(
    "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Sisma_three_components.jpg/500px-Sisma_three_components.jpg",
    caption="Exemple de sismogramme : enregistrement d'un séisme sur trois axes",
    use_container_width=True
)

st.write("""
En étudiant ces signaux, on peut :
- Détecter un séisme
- Trouver l'heure et le lieu du séisme
- Mesurer sa puissance

**Exemple d'activité:**
- On observe un signal sismique sur plusieurs stations.
- On repère l'arrivée des ondes P et S.
- On utilise la différence de temps d'arrivée pour localiser l'épicentre.

👉 Passe à la page suivante pour explorer comment on passe du signal au séisme!
""")

st.subheader("Quiz final : Que peux-tu faire avec les signaux sismiques ?")
quiz = st.multiselect(
    "Coche toutes les bonnes réponses :",
    [
        "Détecter un séisme",
        "Mesurer la température du sol",
        "Trouver l'heure et le lieu du séisme",
        "Mesurer la puissance du séisme",
        "Prévoir la météo"
    ]
)
if st.button("Vérifier le quiz final"):
    bonnes = {"Détecter un séisme", "Trouver l'heure et le lieu du séisme", "Mesurer la puissance du séisme"}
    if set(quiz) == bonnes:
        st.success("Parfait ! Tu es prêt(e) pour la suite.")
    else:
        st.warning("Il y a des erreurs ou des oublis. Relis bien la page !")

st.info("Retrouve les liens entre séismes et signaux dans les autres pages du menu.")