import streamlit as st
from pyproj import Transformer
import folium
from streamlit_folium import st_folium
from streamlit_javascript import st_javascript

st.set_page_config(page_title="PPM België GPS/Handmatig", layout="centered")
st.title("PPM Berekening België 🇧🇪")

# Belgische Y/Z waarden
Y_vals = [242000,238000,234000,230000,226000,221000,217000,212000,
          207000,201000,195000,188000,180000,171000,157000,151000,
          141000,138000,132000,123000,113000,104000,95000,86000,
          76000,67000,58000,49000,39500,30500,21000]

# --- PPM Berekeningsfunctie ---
def bereken_ppm_be(Y, Z):
    if Y > Y_vals[0] or Y < Y_vals[-1]:
        st.warning("Y-coördinaat buiten bereik (21000 - 242000)")
        return None

    # Yppm berekening (zelfde als eerder)
    if Y >= Y_vals[1] and Y <= Y_vals[0]:
        Yppm = ((Y - Y_vals[1]) * 10 / 4000 + 70)
    elif Y >= Y_vals[2] and Y < Y_vals[1]:
        Yppm = ((Y - Y_vals[2]) * 10 / 4000 + 60)
    elif Y >= Y_vals[3] and Y < Y_vals[2]:
        Yppm = ((Y - Y_vals[3]) * 10 / 4000 + 50)
    elif Y >= Y_vals[4] and Y < Y_vals[3]:
        Yppm = ((Y - Y_vals[4]) * 10 / 4000 + 40)
    elif Y >= Y_vals[5] and Y < Y_vals[4]:
        Yppm = ((Y - Y_vals[5]) * 10 / 5000 + 30)
    elif Y >= Y_vals[6] and Y < Y_vals[5]:
        Yppm = ((Y - Y_vals[6]) * 10 / 4000 + 20)
    elif Y >= Y_vals[7] and Y < Y_vals[6]:
        Yppm = ((Y - Y_vals[7]) * 10 / 5000 + 10)
    elif Y >= Y_vals[8] and Y < Y_vals[7]:
        Yppm = ((Y - Y_vals[8]) * 10 / 5000 + 0)
    elif Y >= Y_vals[9] and Y < Y_vals[8]:
        Yppm = ((Y - Y_vals[9]) * 10 / 6000 - 10)
    elif Y >= Y_vals[10] and Y < Y_vals[9]:
        Yppm = ((Y - Y_vals[10]) * 10 / 6000 - 20)
    elif Y >= Y_vals[11] and Y < Y_vals[10]:
        Yppm = ((Y - Y_vals[11]) * 10 / 7000 - 30)
    elif Y >= Y_vals[12] and Y < Y_vals[11]:
        Yppm = ((Y - Y_vals[12]) * 10 / 8000 - 40)
    elif Y >= Y_vals[13] and Y < Y_vals[12]:
        Yppm = ((Y - Y_vals[13]) * 10 / 9000 - 50)
    elif Y >= Y_vals[14] and Y < Y_vals[13]:
        Yppm = ((Y - Y_vals[14]) * 10 / 14000 - 60)
    elif Y >= Y_vals[15] and Y < Y_vals[14]:
        Yppm = ((Y - Y_vals[15]) * 3 / 6000 - 63)
    elif Y >= Y_vals[16] and Y < Y_vals[15]:
        Yppm = ((Y - Y_vals[16]) * 3 / 10000 - 66)
    elif Y >= Y_vals[17] and Y < Y_vals[16]:
        Yppm = ((Y - Y_vals[17]) * 1 / 3000 - 67)
    elif Y >= Y_vals[18] and Y < Y_vals[17]:
        Yppm = ((Y - Y_vals[18]) * 1 / 6000 - 68)
    elif Y >= Y_vals[19] and Y < Y_vals[18]:
        Yppm = ((Y - Y_vals[19]) * (-2) / 9000 - 66)
    elif Y >= Y_vals[20] and Y < Y_vals[19]:
        Yppm = ((Y - Y_vals[20]) * (-4) / 10000 - 62)
    elif Y >= Y_vals[21] and Y < Y_vals[20]:
        Yppm = ((Y - Y_vals[21]) * (-4) / 9000 - 58)
    elif Y >= Y_vals[22] and Y < Y_vals[21]:
        Yppm = ((Y - Y_vals[22]) * (-7) / 9000 - 51)
    elif Y >= Y_vals[23] and Y < Y_vals[22]:
        Yppm = ((Y - Y_vals[23]) * (-10) / 9000 - 41)
    elif Y >= Y_vals[24] and Y < Y_vals[23]:
        Yppm = ((Y - Y_vals[24]) * (-12) / 10000 - 29)
    elif Y >= Y_vals[25] and Y < Y_vals[24]:
        Yppm = ((Y - Y_vals[25]) * (-13) / 9000 - 16)
    elif Y >= Y_vals[26] and Y < Y_vals[25]:
        Yppm = ((Y - Y_vals[26]) * (-16) / 9000 + 0)
    elif Y >= Y_vals[27] and Y < Y_vals[26]:
        Yppm = ((Y - Y_vals[27]) * (-18) / 9000 + 18)
    elif Y >= Y_vals[28] and Y < Y_vals[27]:
        Yppm = ((Y - Y_vals[28]) * (-20) / 9500 + 38)
    elif Y >= Y_vals[29] and Y < Y_vals[28]:
        Yppm = ((Y - Y_vals[29]) * (-22) / 9000 + 60)
    elif Y >= Y_vals[30] and Y < Y_vals[29]:
        Yppm = ((Y - Y_vals[30]) * (-24) / 9500 + 84)

    # Zppm (zelfde als eerder)
    if 0 <= Z <= 10:
        Zppm = ((10-Z)*2/10 + (-2))
    elif 10 < Z <= 50:
        Zppm = ((50-Z)*6/40 + (-8))
    elif 50 < Z <= 100:
        Zppm = ((100-Z)*8/50 + (-16))
    elif 100 < Z <= 150:
        Zppm = ((150-Z)*8/50 + (-24))
    elif 150 < Z <= 200:
        Zppm = ((200-Z)*7/50 + (-32))
    elif 200 < Z <= 250:
        Zppm = ((250-Z)*8/50 + (-39))
    elif 250 < Z <= 300:
        Zppm = ((300-Z)*8/50 + (-47))
    elif 300 < Z <= 350:
        Zppm = ((350-Z)*8/50 + (-55))
    elif 350 < Z <= 400:
        Zppm = ((400-Z)*8/50 + (-63))
    elif 400 < Z <= 450:
        Zppm = ((450-Z)*8/50 + (-71))
    elif 450 < Z <= 500:
        Zppm = ((500-Z)*7/50 + (-78))
    elif 500 < Z <= 550:
        Zppm = ((550-Z)*8/50 + (-86))
    elif 550 < Z <= 600:
        Zppm = ((600-Z)*8/50 + (-94))
    elif 600 < Z <= 650:
        Zppm = ((650-Z)*8/50 + (-102))
    elif 650 < Z <= 700:
        Zppm = ((700-Z)*8/50 + (-110))
    else:
        Zppm = 0

    return round(Yppm + Zppm)

# --- Keuze: GPS of Handmatig ---
use_gps = st.checkbox("Gebruik GPS-locatie?", value=False)

if use_gps:
    coords = st_javascript("navigator.geolocation.getCurrentPosition(pos => pos.coords)")
    if coords:
        lat = coords['latitude']
        lon = coords['longitude']
        transformer = Transformer.from_crs("EPSG:4326", "EPSG:31370")
        Y_be, Z_be = transformer.transform(lat, lon)
        Y_be = round(Y_be, 0)
        Z_be = round(Z_be, 0)
        ppm_value = bereken_ppm_be(Y_be, Z_be)
        if ppm_value is not None:
            st.success(f"PPM op basis van GPS: {ppm_value} ppm")
            m = folium.Map(location=[lat, lon], zoom_start=14)
            folium.Marker([lat, lon], tooltip=f"PPM: {ppm_value}").add_to(m)
            st_folium(m, width=700, height=500)
else:
    Y_manual = st.number_input("Handmatige Y-coördinaat", value=0, step=1000)
    Z_manual = st.number_input("Handmatige Z-coördinaat", value=0, step=10)
    if st.button("Bereken PPM"):
        ppm_value = bereken_ppm_be(Y_manual, Z_manual)
        if ppm_value is not None:
            st.success(f"PPM op basis van handmatige invoer: {ppm_value} ppm")
