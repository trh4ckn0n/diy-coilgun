import os
import json
import random
import streamlit_authenticator as stauth
from dotenv import load_dotenv
import streamlit as st

# Charger variables d'environnement
load_dotenv()

# Configuration Streamlit Authenticator
hashed_passwords = stauth.Hasher([os.getenv("APP_PASSWORD", "trkntrkn")]).generate()

config = {
    "credentials": {
        "usernames": {
            "trhacknon": {
                "email": "you@example.com",
                "name": "Trhacknon",
                "password": hashed_passwords[0]
            }
        }
    },
    "cookie": {
        "name": "coilgun_app_cookie",
        "key": "abcdef",  # à changer pour un vrai secret
        "expiry_days": 1
    },
    "preauthorized": {
        "emails": ["you@example.com"]
    }
}

# Authentificateur
authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
    config["preauthorized"]
)

# UI de login
with st.sidebar:
    st.image("https://media.giphy.com/media/zOvBKUUEERdNm/giphy.gif", use_column_width=True)
    name, auth_status, username = authenticator.login("🔐 Connexion", "sidebar")

if auth_status is None:
    st.warning("👉 Veuillez vous connecter via la barre latérale.")
    st.stop()
elif not auth_status:
    st.error("❌ Identifiants incorrects.")
    st.stop()

# Déconnexion dans la sidebar
with st.sidebar:
    authenticator.logout("🚪 Déconnexion", "sidebar")
    st.success(f"✅ Connecté : {name}")

# Protection SEO + iframes
st.markdown("""
    <meta name="robots" content="noindex">
    <style>iframe, embed, object { display: none !important; }</style>
    <script>document.addEventListener('DOMContentLoaded', function () { document.referrer = ''; });</script>
""", unsafe_allow_html=True)

# Thème dark + header animé
st.markdown("""
<style>
body, .stApp {
    background-color: #0d1117;
    color: #39ff14;
}
.stMarkdown h1, .stMarkdown h2, .stMarkdown h3 {
    color: #39ff14;
}
</style>
<marquee behavior="alternate" scrollamount="5" style="color:#39ff14;font-size:18px;">
⚡️ Interface avancée Coilgun DIY by trhacknon ⚡️
</marquee>
""", unsafe_allow_html=True)

# Titre & description
st.title("Interface Coilgun DIY - trhacknon")
st.markdown("""
**Configure ton railgun 😎**

Choisis un mode :
- 🔋 **Puissance maximale** (priorité aux performances)
- 💸 **Budget limité** (optimisé pour bas prix)
- 🚗 **Matériel que j'ai déjà** (suggère en fonction de dispo)
""")

# Choix du mode
mode = st.selectbox("Choix du mode", ["Puissance maximale", "Budget limité", "Matériel disponible"])

user_items = []
if mode == "Matériel disponible":
    user_input = st.text_area("Entre ton matériel (1 par ligne)", "18650\npiles 9v\ncondensateur 4700uF\nfil cuivre 0.5mm")
    user_items = [i.strip().lower() for i in user_input.splitlines() if i.strip()]

# Génération de config
if mode == "Puissance maximale":
    config_finale = {
        "batterie": "2x 18650 Li-Ion 7.4V",
        "condensateur": "10000uF 25V",
        "bobine": "Fil cuivre 0.6mm, 800 tours",
        "interrupteur": "MOSFET IRF540N",
        "tube": "PVC rigide 12mm",
        "projectile": "clou acier 6cm",
        "resistance": "10 ohm 5W pour charge progressive"
    }
elif mode == "Budget limité":
    config_finale = {
        "batterie": "Pile 9V (x2 si possible)",
        "condensateur": "4700uF 16V",
        "bobine": "Fil cuivre 0.4mm, 600 tours",
        "interrupteur": "Switch classique bouton poussoir",
        "tube": "Stylo vide",
        "projectile": "clou 5cm",
        "resistance": "Résistance 20 ohm 2W"
    }
else:
    config_finale = {
        "batterie": "2x 18650" if "18650" in user_items else "Pile 9V",
        "condensateur": "10000uF 25V" if any("10000" in i or "25v" in i for i in user_items) else "4700uF 16V",
        "bobine": "Fil cuivre 0.5mm, 700 tours" if any("cuivre" in i for i in user_items) else "Fil 0.4mm, 600 tours",
        "interrupteur": "MOSFET IRF540N" if "mosfet" in user_items else "Switch standard",
        "tube": "Stylo vide" if "stylo" in user_items else "Tube PVC 10-12mm",
        "projectile": "Clou acier 5-6cm",
        "resistance": "10 ohm 5W"
    }

# Affichage config
st.subheader("📦 Configuration recommandée")
st.json(config_finale)

# Liste achat avec liens Amazon
st.subheader("🛒 Matériel recommandé (liens Amazon)")
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

# Affichage dynamique
for k, v in config_finale.items():
    link = None
    if "18650" in v.lower():
        link = base_links["18650"]
    elif "pile 9v" in v.lower():
        link = base_links["pile 9v"]
    elif "condensateur" in k.lower():
        link = base_links["condensateur"]
    elif "fil" in v.lower():
        link = base_links["fil cuivre"]
    elif "mosfet" in v.lower():
        link = base_links["mosfet"]
    elif "switch" in v.lower() or "interrupteur" in v.lower():
        link = base_links["switch"]
    elif "pvc" in v.lower():
        link = base_links["tube pvc"]
    elif "clou" in v.lower():
        link = base_links["clou"]
    elif "resistance" in v.lower():
        link = base_links["resistance"]

    if link:
        st.markdown(f"- **{k.capitalize()} :** [{v}]({link})")

# Export JSON de config
if st.checkbox("📄 Afficher JSON exportable"):
    st.code(json.dumps({
        "config": config_finale,
        "mode": mode,
        "id": random.randint(1000, 9999)
    }, indent=4), language="json")
