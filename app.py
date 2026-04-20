import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Cigar Connoisseur", page_icon="🍂", layout="centered")
st.title("🍂 Cigar Connoisseur")


# ====================== CSV LADEN ======================
@st.cache_data(ttl=10)
def load_data():
    file_path = "cigars.csv"
    if not os.path.exists(file_path):
        st.error("❌ Datei 'cigars.csv' nicht gefunden!")
        st.stop()

    df = pd.read_csv(file_path, sep=";", encoding="utf-8", na_filter=False)
    df = df.fillna('')
    df = df.map(lambda x: str(x).strip() if isinstance(x, str) else x)
    return df


df = load_data()

# ====================== SUCHE ======================
st.subheader("Wähle deine Zigarre")
search = st.text_input("🔎 Suche nach Zigarre oder Marke", "").strip()

if search:
    mask = (
            df["Zigarre"].str.contains(search, case=False, na=False) |
            df["Marke"].str.contains(search, case=False, na=False)
    )
    filtered = df[mask]
else:
    filtered = df

filtered = filtered.sort_values(by="Zigarre")

if filtered.empty:
    st.warning("Keine passende Zigarre gefunden.")
else:
    selected = st.selectbox("Zigarre auswählen", filtered["Zigarre"].tolist())

    if selected:
        row = df[df["Zigarre"] == selected].iloc[0]

        st.markdown(f"### {row['Zigarre']}")

        # Neue schöne Zeile: Stärke + Geschmacksprofil (kursiv)
        strength = row.get("Stärke", "")
        profile = row.get("Geschmacksprofil", "")
        if strength or profile:
            st.markdown(f"*{strength} – {profile}*")


        # 3 Getränke pro Kategorie
        def show_three_drinks(title, column_name, emoji):
            drinks = row.get(column_name, "")
            drink_list = [d.strip() for d in drinks.split("|") if d.strip()]
            if len(drink_list) < 3:
                drink_list += ["—"] * (3 - len(drink_list))

            st.markdown(f"**{emoji} {title}**")
            for drink in drink_list[:3]:
                st.write(f"• **{drink}**")


        col1, col2, col3 = st.columns(3)
        with col1:
            show_three_drinks("Gentleman", "Gentleman_Drink", "👔")
        with col2:
            show_three_drinks("Lady", "Lady_Drink", "💃")
        with col3:
            show_three_drinks("Geheim-Tipp", "Secret_Tip", "🔥")

        st.success(f"Perfekt für die Lounge! 🍂🥃 – {datetime.now().strftime('%H:%M')}")

# ====================== NEUES PAIRING ======================
st.markdown("---")
st.subheader("Neues Pairing hinzufügen")
with st.expander("Neue Zigarre + 3 Drinks pro Kategorie"):
    with st.form("add_pairing"):
        new_zigarre = st.text_input("Zigarre *")
        new_marke = st.text_input("Marke")
        new_jahr = st.number_input("Jahr", value=2025, step=1)
        new_staerke = st.selectbox("Stärke", ["Mild", "Medium", "Medium-Full", "Full"])
        new_geschmacksprofil = st.text_input("Geschmacksprofil (kurz, z.B. Erdig, fruchtig, Kakao, Vanille)")

        st.markdown("**3 Gentleman-Drinks** (mit ` | ` trennen)")
        g1 = st.text_input("Gentleman 1")
        g2 = st.text_input("Gentleman 2")
        g3 = st.text_input("Gentleman 3")

        st.markdown("**3 Lady-Drinks** (mit ` | ` trennen)")
        l1 = st.text_input("Lady 1")
        l2 = st.text_input("Lady 2")
        l3 = st.text_input("Lady 3")

        st.markdown("**3 Geheim-Tipps** (mit ` | ` trennen)")
        s1 = st.text_input("Secret Tip 1")
        s2 = st.text_input("Secret Tip 2")
        s3 = st.text_input("Secret Tip 3")

        submitted = st.form_submit_button("In CSV speichern")
        if submitted and new_zigarre:
            new_row = pd.DataFrame([{
                "Zigarre": new_zigarre,
                "Marke": new_marke,
                "Jahr": new_jahr,
                "Stärke": new_staerke,
                "Geschmacksprofil": new_geschmacksprofil,
                "Gentleman_Drink": f"{g1} | {g2} | {g3}",
                "Lady_Drink": f"{l1} | {l2} | {l3}",
                "Secret_Tip": f"{s1} | {s2} | {s3}"
            }])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv("cigars.csv", index=False, sep=";", encoding="utf-8")
            st.success("✅ Gespeichert!")
            st.rerun()

with st.sidebar:
    if st.button("🔄 Cache leeren & neu laden"):
        st.cache_data.clear()
        st.rerun()