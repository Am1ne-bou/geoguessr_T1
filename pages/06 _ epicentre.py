import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import st_folium
import plotly.graph_objs as go
import scipy as sp
from plotly.subplots import make_subplots 

def bandpass_filter(data, lowcut, highcut, fs, order=1):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = sp.signal.butter(order, [low, high], btype='band')
    return sp.signal.filtfilt(b, a, data)

# Calcul de l'énergie de l'enveloppe du signal
def compute_energy_envelope(filtered_signal, fs, window_sec=0.5):
    window_size = int(window_sec * fs)
    energy = np.convolve(np.abs(filtered_signal)**2, np.ones(window_size), mode='same')
    return energy / np.max(energy)  # normalisé


# Exemple de données de stations
stations = pd.DataFrame({
    'nom': ['Station A', 'Station B', 'Station C', 'Station D', 'Station E'],
    'lat': [40.59, 43.04, 45.28, 36.07, 34.69],
    'lon': [141.40, 141.38, 135.7, 129.35, 135.37]
})


#genération de données fictives pour les signaux sismiques
def generate_wave(time, wave_type, start, end):
    sig = np.zeros_like(time)
    
    # Création d'une fenêtre de Hanning pour l'enveloppe
    window_length = int(len(time) * (end-start)/time[-1])
    if window_length > 0:
        hanning_win = sp.signal.windows.hann(window_length * 2)     
        win_start = max(0, int(len(time)*start/time[-1]) - window_length//2)
        win_end = min(len(time), int(len(time)*end/time[-1]) + window_length//2)
        full_window = np.zeros_like(time)
        full_window[win_start:win_end] = hanning_win[:win_end-win_start]
    else:
        full_window = np.ones_like(time)

    if wave_type == 'P':
        # Ondes P 
        for i in range(1000):
            freq = 10 + np.random.normal(0, 1) #10hz
            amp = 10 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)

    elif wave_type == 'S':
        # Ondes S
        for i in range(1000):
            freq = 1 + np.random.normal(0, 0.5) #1hz
            amp = 20 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)

    elif wave_type == 'surface':
        # Ondes de surface
        for i in range(1000): 
            freq = 2 + np.random.normal(0, 0.1)
            amp = 50 * np.random.uniform(0.8, 1.2)
            active = (time >= start) & (time <= end)
            sig += amp * np.cos(2 * np.pi * freq * time) * full_window * np.exp(-0.01*(time-start)*active)

    return sig

# Génération des composantes
def generate_seismic_signal(time,start_p, end_p, start_s, end_s, start_surface, end_surface):
    # Bruit de fond
    noise = np.random.normal(0, 0.1, len(time))
    
    # Génération des ondes
    p_wave = generate_wave(time, 'P', start_p, end_p)  
    s_wave = generate_wave(time, 'S', start_s, end_s)
    surface_wave = generate_wave(time, 'surface', start_surface, end_surface)

    # Composition des signaux par composante
    signal_x = noise + 0.1*p_wave + 0.7*s_wave + 0.4*surface_wave
    signal_y = noise + 0.1*p_wave + 0.9*s_wave + 0.5*surface_wave
    signal_z = noise + 1.0*p_wave + 0.1*s_wave + 0.4*surface_wave
    
    return signal_x, signal_y, signal_z

# Génération des signaux sismiques
@st.cache_data
def get_signaux():
    time = np.linspace(0, 180, 18000)
    signal_A = generate_seismic_signal(time, 5, 20, 68, 90, 90, 170)
    signal_B = generate_seismic_signal(time, 5, 22, 85, 103, 95, 170)
    signal_C = generate_seismic_signal(time, 5, 25, 90, 108, 115, 170)
    signal_D = generate_seismic_signal(time, 5, 22, 80, 102, 108, 170)
    signal_E = generate_seismic_signal(time, 5, 20, 60, 80, 90, 160)
    return time, signal_A, signal_B, signal_C, signal_D, signal_E

time, signal_A, signal_B, signal_C, signal_D, signal_E = get_signaux()
signal_A_x, signal_A_y, signal_A_z = signal_A
signal_B_x, signal_B_y, signal_B_z = signal_B
signal_C_x, signal_C_y, signal_C_z = signal_C
signal_D_x, signal_D_y, signal_D_z = signal_D
signal_E_x, signal_E_y, signal_E_z = signal_E

st.title("Carte des stations sismiques")
vp = 7.3  # km/s
vs = 4 # km/s
factor = 1 / (1/vs - 1/vp)  # Facteur de conversion pour la distance


if "distance A" not in st.session_state:
    st.session_state["distance A"] = 0.0
if "distance B" not in st.session_state:
    st.session_state["distance B"] = 0.0
if "distance C" not in st.session_state:
    st.session_state["distance C"] = 0.0
if "distance D" not in st.session_state:
    st.session_state["distance D"] = 0.0
if "distance E" not in st.session_state:
    st.session_state["distance E"] = 0.0

# Carte folium
m = folium.Map(location=[stations['lat'].mean(), stations['lon'].mean()], zoom_start=4)
for i, row in stations.iterrows():
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=row['nom'],
        tooltip=row['nom'],
    ).add_to(m)
# Ajout des cercles de distance
if st.session_state["distance A"] > 0:
    folium.Circle(
        location=[stations.loc[stations['nom'] == 'Station A', 'lat'].values[0],
                  stations.loc[stations['nom'] == 'Station A', 'lon'].values[0]],
        radius=st.session_state["distance A"] * 1000,  # Convertir km en m
        color='blue',
        stroke=True,
        weight=5,
        opacity=0.2,
        
    ).add_to(m)
if st.session_state["distance B"] > 0:
    folium.Circle(
        location=[stations.loc[stations['nom'] == 'Station B', 'lat'].values[0],
                  stations.loc[stations['nom'] == 'Station B', 'lon'].values[0]],
        radius=st.session_state["distance B"] * 1000,  # Convertir km en m
        color='blue',
        stroke=True,
        weight=5,
        opacity=0.2,
    ).add_to(m)
if st.session_state["distance C"] > 0:
    folium.Circle(
        location=[stations.loc[stations['nom'] == 'Station C', 'lat'].values[0],
                  stations.loc[stations['nom'] == 'Station C', 'lon'].values[0]],
        radius=st.session_state["distance C"] * 1000,  # Convertir km en m
        color='blue',
        stroke=True,
        weight=5,
        opacity=0.2,
    ).add_to(m)
if st.session_state["distance D"] > 0:
    folium.Circle(
        location=[stations.loc[stations['nom'] == 'Station D', 'lat'].values[0],
                  stations.loc[stations['nom'] == 'Station D', 'lon'].values[0]],
        radius=st.session_state["distance D"] * 1000,  # Convertir km en m
        color='blue',
        stroke=True,
        weight=5,
        opacity=0.2,
    ).add_to(m)
if st.session_state["distance E"] > 0:
    folium.Circle(
        location=[stations.loc[stations['nom'] == 'Station E', 'lat'].values[0],
                  stations.loc[stations['nom'] == 'Station E', 'lon'].values[0]],
        radius=st.session_state["distance E"] * 1000,  # Convertir km en m
        color='blue',
        stroke=True,
        weight=5,
        opacity=0.2,
    ).add_to(m)


# Affichage de la carte et récupération du clic
st.write("Cliquez sur une station pour afficher ses signaux sismiques.")
map_data = st_folium(m, width=700, height=400)

# Sélection de la station (par nom ou clic)
selected_station = st.selectbox("Ou choisissez une station :", stations['nom'])

# (Ici, tu peux remplacer par la détection du clic sur la carte si tu veux aller plus loin)


st.subheader(f"Signaux sismiques collectés à {selected_station}")

if selected_station == 'Station A':
    signal_x, signal_y, signal_z = signal_A_x, signal_A_y, signal_A_z
elif selected_station == 'Station B':
    signal_x, signal_y, signal_z = signal_B_x, signal_B_y, signal_B_z
elif selected_station == 'Station C':
    signal_x, signal_y, signal_z = signal_C_x, signal_C_y, signal_C_z
elif selected_station == 'Station D':
    signal_x, signal_y, signal_z = signal_D_x, signal_D_y, signal_D_z
elif selected_station == 'Station E':
    signal_x, signal_y, signal_z = signal_E_x, signal_E_y, signal_E_z

fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=time, y=signal_x+signal_y+signal_z, mode='lines', name='Signal combiné',line=dict(color='purple')))
fig1.update_layout(
    title="Signal combiné (X + Y + Z)",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
) 


# Création de la figure avec subplots liés
fig_combined = make_subplots(
    rows=3, cols=1,
    subplot_titles=("Composante Nord-Sud (X)", "Composante Est-Ouest (Y)", "Composante Verticale (Z)"),
    vertical_spacing=0.1,
    shared_xaxes=True  
)

# Ajout des traces
fig_combined.add_trace(
    go.Scatter(x=time, y=signal_x, mode='lines', name='X', line=dict(color='blue')),
    row=1, col=1
)

fig_combined.add_trace(
    go.Scatter(x=time, y=signal_y, mode='lines', name='Y', line=dict(color='red')),
    row=2, col=1
)

fig_combined.add_trace(
    go.Scatter(x=time, y=signal_z, mode='lines', name='Z', line=dict(color='lime')),
    row=3, col=1
)

# Configuration du layout
fig_combined.update_layout(
    height=900,
    showlegend=False,
    template="plotly_white",
    xaxis=dict(matches='x2'),
    xaxis2=dict(matches='x3')
)

# Configuration des axes
fig_combined.update_xaxes(title_text="Temps (s)", row=3, col=1)
fig_combined.update_yaxes(title_text="Amplitude X", row=1, col=1)
fig_combined.update_yaxes(title_text="Amplitude Y", row=2, col=1)
fig_combined.update_yaxes(title_text="Amplitude Z", row=3, col=1)

fig_combined.update_layout(
    title="Comparaison des signaux sismiques (X, Y, Z)",
    xaxis_title="Temps (s)",
    yaxis_title="Amplitude",
    template="plotly_white"
)
if st.button("Afficher les signaux sismiques"):
    st.subheader(f"Signaux sismiques de {selected_station}")

    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("""Comparaison le temps de depart des signaux X, Y et Z""")
    st.plotly_chart(fig_combined, use_container_width=True)


st.write(
    """ Choisissez le signal à analyser :
    """)
signal_choice = st.selectbox("Sélectionnez le signal", ("Nord-Sud", "Est-Ouest", "Vertical"))
fs=110

if signal_choice == "Nord-Sud":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_x = go.Figure()
    signal_s = bandpass_filter(signal_x, 0.5, 2, fs)  # Onde S

    energie_s = compute_energy_envelope(signal_s, fs)

    
    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_s_x=st.slider(
        "Temps d'arrivée de l'onde S (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="cyan", annotation_text="Onde S")
    if st.button("Verification des temps d'arrivée de l'onde S"):
        signal_s = bandpass_filter(signal_x, 0.5, 2, fs)  # Onde S

        energie_s = compute_energy_envelope(signal_s, fs)

        # Détection de pics
        peaks_s, _ = sp.signal.find_peaks(energie_s, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='blue')))
        
        if  len(peaks_s) > 0:
            t_s_x = time[peaks_s[0]]

            
            st.success(f"🟣 Onde S détectée à t = {t_s_x:.2f} s (≈1 Hz)")

            fig_puissance_x.add_vline(x=t_s_x, line_dash="dash", line_color="purple", annotation_text="Onde S")
            

        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_x, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_x.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='blue')))
        st.plotly_chart(fig_puissance_x, use_container_width=True)

    

if signal_choice == "Est-Ouest":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_y = go.Figure()
    signal_s = bandpass_filter(signal_y, 0.5, 2, fs)  # Onde S

    energie_s = compute_energy_envelope(signal_s, fs)

    
    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_s_y=st.slider(
        "Temps d'arrivée de l'onde S (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_y.add_vline(x=t_s_y, line_dash="dash", line_color="orange", annotation_text="Onde S")
    if st.button("Verification des temps d'arrivée de l'onde S"):
        signal_s = bandpass_filter(signal_y, 0.5, 2, fs)  # Onde S

        energie_s = compute_energy_envelope(signal_s, fs)

        # Détection de pics
        peaks_s, _ = sp.signal.find_peaks(energie_s, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='red')))

        if  len(peaks_s) > 0:
            t_s_y = time[peaks_s[0]]


            st.success(f"🟣 Onde S détectée à t = {t_s_y:.2f} s (≈1 Hz)")

            fig_puissance_y.add_vline(x=t_s_y, line_dash="dash", line_color="purple", annotation_text="Onde S")


        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_y, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_y.add_trace(go.Scatter(x=time, y=energie_s, mode='lines', name='Énergie onde S', line=dict(color='red')))
        st.plotly_chart(fig_puissance_y, use_container_width=True)


if signal_choice == "Vertical":
    # Filtrage dans les bandes typiques des ondes P et S
    fig_puissance_z = go.Figure()
    signal_p = bandpass_filter(signal_z, 8, 12, fs)  # Onde P

    energie_p = compute_energy_envelope(signal_p, fs)

    #Temps d'arrivée des ondes P et S avant verification donne par l'utilisateur

    t_p_z=st.slider(
        "Temps d'arrivée de l'onde P (en secondes)",
        min_value=float(time[0]),
        max_value=float(time[-1]),
        value=(float(time[0])),
        step=0.1,
        key='slider_ts'
    )
    fig_puissance_z.add_vline(x=t_p_z, line_dash="dash", line_color="yellow", annotation_text="Onde P")
    if st.button("Verification des temps d'arrivée de l'onde P"):
        signal_p = bandpass_filter(signal_z, 8, 12, fs)  # Onde P

        energie_p = compute_energy_envelope(signal_p, fs)

        # Détection de pics
        peaks_p, _ = sp.signal.find_peaks(energie_p, height=0.05, distance=int(0.3 * fs))

        # Traces de l’énergie et des pics
        fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='green')))

        if  len(peaks_p) > 0:
            t_p_x = time[peaks_p[0]]


            st.success(f"🟢 Onde P détectée à t = {t_p_x:.2f} s (≈10 Hz)")

            fig_puissance_z.add_vline(x=t_p_x, line_dash="dash", line_color="lime", annotation_text="Onde P")


        else:
            st.warning("Impossible de détecter automatiquement les ondes P et S.")

        st.plotly_chart(fig_puissance_z, use_container_width=True)

    else:
        # Traces de l’énergie et des pics
        fig_puissance_z.add_trace(go.Scatter(x=time, y=energie_p, mode='lines', name='Énergie onde P', line=dict(color='green')))
        st.plotly_chart(fig_puissance_z, use_container_width=True)





# Sélection interactive de tp et ts

tp = st.number_input("tp (s)", min_value=float(time[0]), max_value=float(time[-1]), value=10.0, step=0.01)
ts = st.number_input("ts (s)", min_value=float(time[0]), max_value=float(time[-1]), value=30.0, step=0.01)

st.subheader("Calcul de la distance à l'épicentre")
st.write(f"Station sélectionnée : {selected_station}")
if st.button("Calculer la distance à l'épicentre"):
    if ts > tp:
        st.success(f"Δt = ts - tp = {ts-tp:.2f} s")
        vp = 7.3  # km/s
        vs = 4 # km/s
        distance = (ts-tp) / (1/vs - 1/vp)
        st.info(f"Distance estimée à l'épicentre : {distance:.2f} km")
        #Dessin du cercle de distance
        
        if selected_station == 'Station A':
            st.session_state["distance A"] = distance
        elif selected_station == 'Station B':
            st.session_state["distance B"] = distance
        elif selected_station == 'Station C':
            st.session_state["distance C"] = distance
        elif selected_station == 'Station D':
            st.session_state["distance D"] = distance
        elif selected_station == 'Station E':
            st.session_state["distance E"] = distance
        
    else:
        st.warning("ts doit être supérieur à tp.")

