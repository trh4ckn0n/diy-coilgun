import streamlit as st
import os
import json
import random
import streamlit_authenticator as stauth
from dotenv import load_dotenv

load_dotenv()

raw_password = os.getenv("APP_PASSWORD", "trkntrkn")

names = ["Trhacknon"]
usernames = ["trhacknon"]
passwords = [raw_password]

# Générer le hash
hashed_passwords = stauth.Hasher(passwords).generate()

# Correctif ici ↓
authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    cookie_name="coilgun_app_cookie",
    key="abcdef",
    cookie_expiry_days=1
)

name, auth_status, username = authenticator.login("🔐 Connexion", "main")

if auth_status:
    st.success(f"Bienvenue {name} ! Interface disponible.")
elif auth_status is False:
    st.error("Nom d’utilisateur ou mot de passe incorrect")
else:
    st.info("Connexion requise") 

# Protection robots/iframes
st.markdown("""
    <script>document.addEventListener('DOMContentLoaded', function () {document.referrer = '';});</script>
    <style>iframe, embed, object { display: none !important; }</style>
""", unsafe_allow_html=True)
st.markdown('<meta name="robots" content="noindex">', unsafe_allow_html=True)

# Header animé
st.markdown("""
<marquee behavior="alternate" scrollamount="5" style="color:#39ff14;font-size:18px;">
⚡️ Interface avancée Coilgun DIY by trhacknon ⚡️
</marquee>
""", unsafe_allow_html=True)

# Thème visuel
st.markdown("""
<style>
body {background-color: #0d1117; color: #39ff14;}
.stApp {background-color: #0d1117;}
</style>
""", unsafe_allow_html=True)

# Interface principale
st.title("Interface Coilgun DIY - trhacknon")
st.markdown("""
**Configure ton railgun 😎**

Choisis un mode :
- 🔋 **Puissance maximale** (priorité aux performances)
- 💸 **Budget limité** (optimisé pour bas prix)
- 🚗 **Matériel que j'ai déjà** (suggère en fonction de dispo)
""")

mode = st.selectbox("Choix du mode", ["Puissance maximale", "Budget limité", "Matériel disponible"])

user_items = []
if mode == "Matériel disponible":
    user_items = st.text_area("Entre ton matériel (1 par ligne)", "18650\npiles 9v\ncondensateur 4700uF\nfil cuivre 0.5mm")
    user_items = [i.strip().lower() for i in user_items.splitlines() if i.strip() != ""]

# Config selon mode
if mode == "Puissance maximale":
    config = {
        "batterie": "2x 18650 Li-Ion 7.4V",
        "condensateur": "10000uF 25V",
        "bobine": "Fil cuivre 0.6mm, 800 tours",
        "interrupteur": "MOSFET IRF540N",
        "tube": "PVC rigide 12mm",
        "projectile": "clou acier 6cm",
        "resistance": "10 ohm 5W pour charge progressive"
    }
elif mode == "Budget limité":
    config = {
        "batterie": "Pile 9V (x2 si possible)",
        "condensateur": "4700uF 16V",
        "bobine": "Fil cuivre 0.4mm, 600 tours",
        "interrupteur": "Switch classique bouton poussoir",
        "tube": "Stylo vide",
        "projectile": "clou 5cm",
        "resistance": "Résistance 20 ohm 2W"
    }
else:
    config = {
        "batterie": "2x 18650" if "18650" in user_items else "Pile 9V",
        "condensateur": "10000uF 25V" if any("10000" in i or "25v" in i for i in user_items) else "4700uF 16V",
        "bobine": "Fil cuivre 0.5mm, 700 tours" if any("cuivre" in i for i in user_items) else "Fil 0.4mm, 600 tours",
        "interrupteur": "MOSFET IRF540N" if "mosfet" in user_items else "Switch standard",
        "tube": "Stylo vide" if "stylo" in user_items else "Tube PVC 10-12mm",
        "projectile": "Clou acier 5-6cm",
        "resistance": "10 ohm 5W"
    }

st.subheader("Configuration recommandée")
st.json(config)

# Liste achat
st.subheader("Liste de matos + liens")
base_links = {
    "18650": "https://www.amazon.fr/s?k=18650",
    "pile 9v": "https://www.amazon.fr/s?k=pile+9v",
    "condensateur": "https://www.amazon.fr/s?k=condensateur+10000uf",
    "fil cuivre": "https://www.amazon.fr/s?k=fil+cuivre+emaill%C3%A9",
    "mosfet": "https://www.amazon.fr/s?k=mosfet+irf540n",
    "switch": "https://www.amazon.fr/s?k=interrupteur+bouton+poussoir",
    "tube pvc": "https://www.amazon.fr/s?k=tube+pvc",
    "clou": "https://www.amazon.fr/s?k=clou+acier",
    "resistance": "https://www.amazon.fr/s?k=resistance+5w"
}

for k, v in config.items():
    if "18650" in v:
        st.markdown(f"- **Batterie :** [{v}]({base_links['18650']})")
    elif "pile 9v" in v.lower():
        st.markdown(f"- **Batterie :** [{v}]({base_links['pile 9v']})")
    elif "condensateur" in k:
        st.markdown(f"- **Condensateur :** [{v}]({base_links['condensateur']})")
    elif "fil" in v:
        st.markdown(f"- **Bobine :** [{v}]({base_links['fil cuivre']})")
    elif "mosfet" in v.lower():
        st.markdown(f"- **MOSFET :** [{v}]({base_links['mosfet']})")
    elif "switch" in v.lower() or "interrupteur" in v.lower():
        st.markdown(f"- **Interrupteur :** [{v}]({base_links['switch']})")
    elif "pvc" in v.lower():
        st.markdown(f"- **Tube :** [{v}]({base_links['tube pvc']})")
    elif "clou" in v.lower():
        st.markdown(f"- **Projectile :** [{v}]({base_links['clou']})")
    elif "resistance" in v.lower():
        st.markdown(f"- **Résistance de charge :** [{v}]({base_links['resistance']})")

# Historique JSON
if st.checkbox("Afficher l'historique des configs JSON"):
    st.code(json.dumps({"config": config, "mode": mode, "id": random.randint(1000, 9999)}, indent=4))
