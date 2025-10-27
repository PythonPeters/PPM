# ppm_belgie_realtime_final.py
import streamlit as st
import streamlit_geolocation
from pyproj import Transformer
import folium
from streamlit_folium import st_folium
import time

st.set_page_config(page_title="PPM België Realtime GPS", layout="centered")
st.title("🇧🇪 PPM België")

st.markdown("""
De marker op de kaart volgt je GPS-locatie.  
PPM wordt **realtime bijgewerkt** als je GPS beweegt.  
Handmatige invoer werkt naast GPS, berekening gebeurt pas bij "**bereken PPM**".
""")

# --- Lambert72 transformer ---
transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370", always_xy=True)

# --- Originele PPM functie België ---
def bereken_ppm_belgie_from_YZ(Y, Z):
    Y_vals = [
        242000,238000,234000,230000,226000,221000,217000,212000,
        207000,201000,195000,188000,180000,171000,157000,151000,
        141000,138000,132000,123000,113000,104000,95000,86000,
        76000,67000,58000,49000,39500,30500,21000
    ]
    if Y > Y_vals[0] or Y < Y_vals[-1]:
        return None
    # Originele Yppm berekening
    if Y >= Y_vals[1] and Y <= Y_vals[0]:
        Yppm = (Y - Y_vals[1])*10/4000 + 70
    elif Y >= Y_vals[2] and Y < Y_vals[1]:
        Yppm = (Y - Y_vals[2])*10/4000 + 60
    elif Y >= Y_vals[3] and Y < Y_vals[2]:
        Yppm = (Y - Y_vals[3])*10/4000 + 50
    elif Y >= Y_vals[4] and Y < Y_vals[3]:
        Yppm = (Y - Y_vals[4])*10/4000 + 40
    elif Y >= Y_vals[5] and Y < Y_vals[4]:
        Yppm = (Y - Y_vals[5])*10/5000 + 30
    elif Y >= Y_vals[6] and Y < Y_vals[5]:
        Yppm = (Y - Y_vals[6])*10/4000 + 20
    elif Y >= Y_vals[7] and Y < Y_vals[6]:
        Yppm = (Y - Y_vals[7])*10/5000 + 10
    elif Y >= Y_vals[8] and Y < Y_vals[7]:
        Yppm = (Y - Y_vals[8])*10/5000 + 0
    elif Y >= Y_vals[9] and Y < Y_vals[8]:
        Yppm = (Y - Y_vals[9])*10/6000 - 10
    elif Y >= Y_vals[10] and Y < Y_vals[9]:
        Yppm = (Y - Y_vals[10])*10/6000 - 20
    elif Y >= Y_vals[11] and Y < Y_vals[10]:
        Yppm = (Y - Y_vals[11])*10/7000 - 30
    elif Y >= Y_vals[12] and Y < Y_vals[11]:
        Yppm = (Y - Y_vals[12])*10/8000 - 40
    elif Y >= Y_vals[13] and Y < Y_vals[12]:
        Yppm = (Y - Y_vals[13])*10/9000 - 50
    elif Y >= Y_vals[14] and Y < Y_vals[13]:
        Yppm = (Y - Y_vals[14])*10/14000 - 60
    elif Y >= Y_vals[15] and Y < Y_vals[14]:
        Yppm = (Y - Y_vals[15])*3/6000 - 63
    elif Y >= Y_vals[16] and Y < Y_vals[15]:
        Yppm = (Y - Y_vals[16])*3/10000 - 66
    elif Y >= Y_vals[17] and Y < Y_vals[16]:
        Yppm = (Y - Y_vals[17])*1/3000 - 67
    elif Y >= Y_vals[18] and Y < Y_vals[17]:
        Yppm = (Y - Y_vals[18])*1/6000 - 68
    elif Y >= Y_vals[19] and Y < Y_vals[18]:
        Yppm = (Y - Y_vals[19])*(-2)/9000 - 66
    elif Y >= Y_vals[20] and Y < Y_vals[19]:
        Yppm = (Y - Y_vals[20])*(-4)/10000 - 62
    elif Y >= Y_vals[21] and Y < Y_vals[20]:
        Yppm = (Y - Y_vals[21])*(-4)/9000 - 58
    elif Y >= Y_vals[22] and Y < Y_vals[21]:
        Yppm = (Y - Y_vals[22])*(-7)/9000 - 51
    elif Y >= Y_vals[23] and Y < Y_vals[22]:
        Yppm = (Y - Y_vals[23])*(-10)/9000 - 41
    elif Y >= Y_vals[24] and Y < Y_vals[23]:
        Yppm = (Y - Y_vals[24])*(-12)/10000 - 29
    elif Y >= Y_vals[25] and Y < Y_vals[24]:
        Yppm = (Y - Y_vals[25])*(-13)/9000 - 16
    elif Y >= Y_vals[26] and Y < Y_vals[25]:
        Yppm = (Y - Y_vals[26])*(-16)/9000 + 0
    elif Y >= Y_vals[27] and Y < Y_vals[26]:
        Yppm = (Y - Y_vals[27])*(-18)/9000 + 18
    elif Y >= Y_vals[28] and Y < Y_vals[27]:
        Yppm = (Y - Y_vals[28])*(-20)/9500 + 38
    elif Y >= Y_vals[29] and Y < Y_vals[28]:
        Yppm = (Y - Y_vals[29])*(-22)/9000 + 60
    else:
        Yppm = (Y - Y_vals[30])*(-24)/9500 + 84

    # Zppm
    if Z <= 10 and Z >= 0:
        Zppm = (10 - Z)*2/10 -2
    elif Z <= 50:
        Zppm = (50 - Z)*6/40 -8
    elif Z <= 100:
        Zppm = (100 - Z)*8/50 -16
    elif Z <= 150:
        Zppm = (150 - Z)*8/50 -24
    elif Z <= 200:
        Zppm = (200 - Z)*7/50 -32
    elif Z <= 250:
        Zppm = (250 - Z)*8/50 -39
    elif Z <= 300:
        Zppm = (300 - Z)*8/50 -47
    elif Z <= 350:
        Zppm = (350 - Z)*8/50 -55
    elif Z <= 400:
        Zppm = (400 - Z)*8/50 -63
    elif Z <= 450:
        Zppm = (450 - Z)*8/50 -71
    elif Z <= 500:
        Zppm = (500 - Z)*7/50 -78
    elif Z <= 550:
        Zppm = (550 - Z)*8/50 -86
    elif Z <= 600:
        Zppm = (600 - Z)*8/50 -94
    elif Z <= 650:
        Zppm = (650 - Z)*8/50 -102
    elif Z <= 700:
        Zppm = (700 - Z)*8/50 -110
    else:
        Zppm = -110

    return int(Yppm + Zppm)

# --- Session state initiëren ---
for key in ["gps_lat", "gps_lon", "gps_alt", "Y_manual", "Z_manual", "X_manual"]:
    if key not in st.session_state:
        st.session_state[key] = None if "gps" in key else 0

# --- Handmatige invoer ---
st.subheader("Handmatige invoer (optioneel)")
Y_manual = st.number_input("Y (Northing, m)", value=st.session_state["Y_manual"], step=1000)
Z_manual = st.number_input("Z (hoogte, m)", value=st.session_state["Z_manual"], step=1)
X_manual = st.number_input("X (Easting, m, optioneel)", value=st.session_state["X_manual"], step=1000)

# --- Modus keuze (GPS of handmatig) ---
mode = st.radio("Welke invoer wil je gebruiken?", ("GPS", "Manueel"))

# --- Reset knop ---
if st.button("Reset"):
    st.session_state.update({
        "gps_lat": None, "gps_lon": None, "gps_alt": None,
        "Y_manual": 0, "Z_manual": 0, "X_manual": 0
    })
    st.rerun()

# --- Ophalen GPS realtime ---
loc = streamlit_geolocation._streamlit_geolocation(key="geo")
if loc and loc.get("latitude") and loc.get("longitude"):
    st.session_state["gps_lat"] = loc["latitude"]
    st.session_state["gps_lon"] = loc["longitude"]
    st.session_state["gps_alt"] = loc.get("altitude", 0)

# --- Bepaal gebruikte coördinaten ---
used_lat = st.session_state["gps_lat"]
used_lon = st.session_state["gps_lon"]
alt = st.session_state["gps_alt"]

rd_x = rd_y = None
if used_lat is not None:
    rd_x, rd_y = transformer.transform(used_lon, used_lat)
    rd_x = int(rd_x)
    rd_y = int(rd_y)

if mode == "GPS":
    if rd_x is None:
        st.warning("Geen GPS beschikbaar. Schakel over naar handmatige invoer.")
        st.stop()
    X_used = rd_x
    Y_used = rd_y
    Z_used = int(alt if alt is not None else 0)
else:  # Manueel
    X_used = int(X_manual)
    Y_used = int(Y_manual)
    Z_used = int(Z_manual)

# --- Tonen coördinaten ---
st.subheader("Gebruikte coördinaten")
cols = st.columns(2)
with cols[0]:
    st.write("**WGS84 (GPS)**")
    if used_lat and mode=="GPS":
        st.write(f"Latitude: {used_lat:.6f}")
        st.write(f"Longitude: {used_lon:.6f}")
        st.write(f"Altitude: {alt}")
    else:
        st.write("Geen GPS gebruikt")
with cols[1]:
    st.write("**Lambert72(m)**")
    st.write(f"X = {X_used}")
    st.write(f"Y = {Y_used}")
    st.write(f"Z = {Z_used}")

# --- Kaart realtime ---
st.subheader("Locatiekaart")
if used_lat and mode=="GPS":
    m = folium.Map(location=[used_lat, used_lon], zoom_start=5, tiles=None)
    folium.TileLayer('CartoDB positron', name="CartoDB Positron", control=False).add_to(m)

#    m = folium.Map(location=[used_lat, used_lon], zoom_start=17)
    folium.Marker(
        [used_lat, used_lon],
        popup=f"X={X_used}, Y={Y_used}, Z={Z_used}",
        tooltip="Jouw locatie"
    ).add_to(m)
    st_folium(m, width=350, height=350)

# --- Realtime PPM bij GPS ---
if mode == "GPS" and used_lat:
    ppm = bereken_ppm_belgie_from_YZ(Y_used, Z_used)
    if ppm is not None:
        st.success(f"Realtime PPM = {ppm} ppm")
    else:
        st.error("Y-coördinaat buiten bereik (21.000 - 242.000 m).")

# --- PPM knop voor handmatige invoer ---
if mode == "Manueel":
    if st.button("Bereken PPM"):
        ppm = bereken_ppm_belgie_from_YZ(Y_used, Z_used)
        if ppm is not None:
            st.success(f"PPM = {ppm} ppm")
        else:
            st.error("Y-coördinaat buiten bereik (21.000 - 242.000 m).")

