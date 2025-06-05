import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Localisation de plusieurs séismes avec 9 stations")

# 1. Principe
st.header("1. Principe de localisation de l’épicentre")
st.write("""
Pour localiser un séisme, on utilise les temps d’arrivée des ondes sismiques enregistrés par plusieurs stations.
En connaissant la vitesse de propagation des ondes et la position des stations, on peut calculer la distance parcourue par l’onde jusqu’à chaque station.
L’épicentre se trouve à l’intersection des cercles centrés sur chaque station, de rayon égal à la distance parcourue par l’onde.
Ici, il y a 3 séismes (épicentres) et 9 stations.
""")


st.header("2. Données fournies")
st.write("Pour chaque station, on donne le temps d'arrivée du séisme le plus proche et la vitesse des ondes.")


stations = [
    ("Station 1", 100, 200),
    ("Station 2", 300, 150),
    ("Station 3", 500, 100),
    ("Station 4", 700, 200),
    ("Station 5", 900, 300),
    ("Station 6", 800, 600),
    ("Station 7", 600, 700),
    ("Station 8", 400, 800),
    ("Station 9", 200, 700)
]

# Épicentres (liste de tuples)
epicentres = [
    (250, 400),
    (700, 500),
    (500, 200)
]

v = 6.0  # km/s
t0 = 0.0


def distance(x1, y1, x2, y2):
    return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)

distances = []
temps_arrivee = []
epicentre_associe = []
for nom, x, y in stations:
    dists = [distance(x, y, ex, ey) for ex, ey in epicentres]
    i_epi_min = np.argmin(dists)
    d = dists[i_epi_min]
    t = d / v + t0
    distances.append(d)
    temps_arrivee.append(t)
    epicentre_associe.append(i_epi_min + 1)  # +1 pour l'affichage

st.markdown(f"**Vitesse des ondes sismiques :** {v} km/s (fixée pour l'exercice)")
st.markdown("**Temps d'arrivée du séisme le plus proche pour chaque station :**")
for i, (nom, x, y) in enumerate(stations):
    st.write(f"- {nom} : {temps_arrivee[i]:.2f} s")

with st.expander("Besoin d'un indice ? (afficher la formule)"):
    st.latex(r"d = v \times (t_{\text{arrivée}} - t_0)")


st.header("3. Calculez la distance pour chaque station")
if "show_circles" not in st.session_state:
    st.session_state.show_circles = [False] * len(stations)

user_distances = []
cols = st.columns(9)
for i, (nom, x, y) in enumerate(stations):
    with cols[i]:
        user_distances.append(st.number_input(
            f"Distance {nom} (km)", 0.0, 2000.0, 0.0, 1.0, key=f"d_{i}"
        ))
        if st.button(f"Afficher cercle {nom}", key=f"btn_{i}"):
            st.session_state.show_circles[i] = not st.session_state.show_circles[i] #pour après quand le graphique sera fiat

with st.expander("Afficher la correction des distances"):
    st.markdown("**Distances exactes entre chaque station et son épicentre le plus proche :**")
    for i, (nom, x, y) in enumerate(stations):
        st.write(f"- {nom} → Épicentre {epicentre_associe[i]} : {distances[i]:.1f} km")
