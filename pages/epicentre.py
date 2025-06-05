import numpy as np
import streamlit as st
import plotly.graph_objects as go

st.title("Localisation d’un séisme avec 3 stations")

st.header("1. Principe de localisation de l’épicentre")
st.write(
    """
    Pour localiser l’épicentre d’un séisme, on utilise les temps d’arrivée des ondes sismiques enregistrés par plusieurs stations.
    En connaissant la vitesse de propagation des ondes et la position des stations, on peut calculer la distance parcourue par l’onde jusqu’à chaque station.
    L’épicentre se trouve à l’intersection des cercles centrés sur chaque station, de rayon égal à la distance parcourue par l’onde.
    """
)

st.header("2. Paramètres des stations et du séisme")
st.write("Les coordonnées sont données en kilomètres (km)")

stations = {
    "Station A": {"x": 200, "y": 300},
    "Station B": {"x": 600, "y": 400},
    "Station C": {"x": 400, "y": 700},
}

st.info("Coordonnées des stations (fixées) : A = (200, 300) km | B = (600, 400) km | C = (400, 700) km")
v = 6.0
t0 = 0.0


x_epi_ideal = 400
y_epi_ideal = 400


def calc_distance(x_sta, y_sta, x_epi, y_epi):
    return np.sqrt((x_sta - x_epi)**2 + (y_sta - y_epi)**2)

dA_corr = calc_distance(stations["Station A"]["x"], stations["Station A"]["y"], x_epi_ideal, y_epi_ideal)
dB_corr = calc_distance(stations["Station B"]["x"], stations["Station B"]["y"], x_epi_ideal, y_epi_ideal)
dC_corr = calc_distance(stations["Station C"]["x"], stations["Station C"]["y"], x_epi_ideal, y_epi_ideal)


tA = dA_corr / v + t0
tB = dB_corr / v + t0
tC = dC_corr / v + t0

st.info(f"Vitesse des ondes sismiques : {v} km/s (fixée pour l'exercice)")
st.info(f"Temps d'arrivée à la station A : {tA:.2f} s | B : {tB:.2f} s | C : {tC:.2f} s ")
st.info(f"Temps origine du séisme t₀ : {t0} s (fixé)")

with st.expander("Afficher la formule si besoin"):
    st.latex(r"d = v \times (t_{\text{arrivée}} - t_0)")

st.header("3. Calculez la distance parcourue par l'onde jusqu'à chaque station")
st.write("Entrez la distance (en km) pour chaque station.")

dA_user = st.number_input("Distance onde - Station A (km)", 0.0, 10000.0, 0.0, 1.0, key="dA")
dB_user = st.number_input("Distance onde - Station B (km)", 0.0, 10000.0, 0.0, 1.0, key="dB")
dC_user = st.number_input("Distance onde - Station C (km)", 0.0, 10000.0, 0.0, 1.0, key="dC")

if st.button("Afficher la réponse (distances correctes)"):
    st.success(f"Distance onde - Station A : {dA_corr:.1f} km")
    st.success(f"Distance onde - Station B : {dB_corr:.1f} km")
    st.success(f"Distance onde - Station C : {dC_corr:.1f} km")


def intersection_3cercles(xa, ya, ra, xb, yb, rb, xc, yc, rc):

    A = np.array([
        [2*(xb-xa), 2*(yb-ya)],
        [2*(xc-xa), 2*(yc-ya)]
    ])
    b = np.array([
        ra**2 - rb**2 + xb**2 - xa**2 + yb**2 - ya**2,
        ra**2 - rc**2 + xc**2 - xa**2 + yc**2 - ya**2
    ])
    try:
        sol = np.linalg.lstsq(A, b, rcond=None)[0]
        return sol[0], sol[1]
    except Exception:
        return None, None

xA, yA = stations["Station A"]["x"], stations["Station A"]["y"]
xB, yB = stations["Station B"]["x"], stations["Station B"]["y"]
xC, yC = stations["Station C"]["x"], stations["Station C"]["y"]


x_epi, y_epi = intersection_3cercles(xA, yA, dA_user, xB, yB, dB_user, xC, yC, dC_user)

st.header("4. Visualisation de la localisation (triangulation)")
fig = go.Figure()


theta = np.linspace(0, 2*np.pi, 200)
for name, (x, y, r, color) in zip(
    ["A", "B", "C"],
    [(xA, yA, dA_user, "red"), (xB, yB, dB_user, "blue"), (xC, yC, dC_user, "green")]
):
    fig.add_trace(go.Scatter(
        x=x + r * np.cos(theta),
        y=y + r * np.sin(theta),
        mode="lines",
        name=f"Cercle {name}",
        line=dict(color=color, dash="dot"),
        showlegend=True
    ))
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode="markers+text",
        marker=dict(size=10, color=color),
        text=[f"Station {name}"],
        textposition="top center",
        showlegend=False
    ))


fig.update_layout(
    title="Localisation de l'épicentre par triangulation",
    xaxis_title="x (km)",
    yaxis_title="y (km)",
    template="plotly_white",
    width=700, height=700,
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)
st.plotly_chart(fig, use_container_width=True)

if st.button("Afficher la réponse"):
    st.success(f"Coordonnées de l'épicentre : x = {x_epi_ideal:.1f} km, y = {y_epi_ideal:.1f} km")

st.write(
    """
    Calculez les distances à partir des temps d'arrivée et de la vitesse, puis observez la localisation de l'épicentre.
    Modifiez les distances pour voir comment la localisation change.
    """
)