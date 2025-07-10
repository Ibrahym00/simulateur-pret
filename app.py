import streamlit as st
import plotly.express as px
import pandas as pd
from pret_utils import calculer_mensualite, generer_tableau_amortissement
from export_pdf import generer_pdf

st.set_page_config(page_title="Simulateur de Prêt Bancaire", layout="centered")

st.title("🏦 Simulateur de Prêt Bancaire")
st.markdown("Calculez facilement vos mensualités avec ou sans assurance, et visualisez votre tableau d'amortissement.")

# ───────────────────────────────────────────────
# 🔢 Saisie des données
st.header("1️⃣ Paramètres du prêt")

col1, col2 = st.columns(2)
with col1:
    capital = st.number_input("💶 Montant total du bien (EUR)", min_value=1000, step=1000)
    apport = st.number_input("💸 Apport personnel (EUR)", min_value=0, step=500)

with col2:
    taux = st.number_input("📈 Taux d'intérêt annuel (%)", min_value=0.0, format="%.2f")
    taux_assurance = st.number_input("🛡️ Taux assurance (%)", min_value=0.0, format="%.2f")
    duree = st.slider("⏳ Durée du prêt (en années)", min_value=1, max_value=30)

capital_emprunte = capital - apport

if st.button("🚀 Calculer les mensualités"):
    if capital_emprunte <= 0:
        st.error("L'apport ne peut pas être supérieur ou égal au montant total du bien.")
    else:
        mensualite, total, interets = calculer_mensualite(capital_emprunte, taux, duree)
        mensualite_assurance = (capital_emprunte * taux_assurance / 100) / 12
        cout_total_assurance = mensualite_assurance * duree * 12
        mensualite_totale = mensualite + mensualite_assurance

        st.header("📋 Résumé du prêt")
        st.markdown(f"""
        - 🏠 **Montant du bien :** {capital:,.2f} EUR
        - 💸 **Apport personnel :** {apport:,.2f} EUR
        - 🧾 **Montant emprunté :** {capital_emprunte:,.2f} EUR
        - 📆 **Durée :** {duree} ans ({duree * 12} mois)
        - 📈 **Taux d'intérêt :** {taux:.2f} %
        - 🛡️ **Taux assurance :** {taux_assurance:.2f} %
        """)

        st.success(f"💰 Mensualité de crédit seule : **{mensualite:.2f} EUR / mois**")
        st.info(f"📊 Coût total du prêt (hors assurance) : **{total:.2f} EUR**")
        st.warning(f"💸 Intérêts totaux à payer : **{interets:.2f} EUR**")

        st.subheader("🛡️ Assurance emprunteur")
        st.info(f"📌 Mensualité assurance : **{mensualite_assurance:.2f} EUR**")
        st.info(f"📌 Coût total assurance : **{cout_total_assurance:.2f} EUR**")
        st.success(f"💶 **Mensualité totale (prêt + assurance) : {mensualite_totale:.2f} EUR / mois**")

        df_amort = generer_tableau_amortissement(capital_emprunte, taux, duree)
        st.subheader("📅 Tableau d'amortissement")
        st.dataframe(df_amort, use_container_width=True)

        csv = df_amort.to_csv(index=False).encode('utf-8')
        st.download_button("📥 Télécharger le tableau (CSV)", data=csv, file_name="amortissement.csv", mime="text/csv")

        st.subheader("📈 Évolution du prêt dans le temps")

        df_long = pd.melt(df_amort, id_vars="Mois", value_vars=["Intérêt payé (EUR)", "Capital remboursé (EUR)"],
                          var_name="Type", value_name="Montant (EUR)")

        fig = px.area(df_long, x="Mois", y="Montant (EUR)", color="Type",
                      title="Répartition mensuelle des remboursements", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

        fig2 = px.line(df_amort, x="Mois", y="Capital restant dû (EUR)",
                       title="📉 Capital restant dû au fil des mois", template="plotly_white")
        st.plotly_chart(fig2, use_container_width=True)

        st.subheader("📄 Télécharger le rapport PDF")

        resume_dict = {
            "Montant total du bien (EUR)": capital,
            "Apport personnel (EUR)": apport,
            "Montant emprunté (EUR)": capital_emprunte,
            "Durée (années)": duree,
            "Taux d'intérêt (%)": taux,
            "Taux assurance (%)": taux_assurance,
            "Mensualité crédit (EUR)": round(mensualite, 2),
            "Mensualité assurance (EUR)": round(mensualite_assurance, 2),
            "Mensualité totale (EUR)": round(mensualite_totale, 2),
            "Coût total du prêt (EUR)": round(total, 2),
            "Coût total assurance (EUR)": round(cout_total_assurance, 2),
        }

        pdf_bytes = generer_pdf(resume_dict, df_amort)
        st.download_button("📥 Télécharger le PDF", data=pdf_bytes, file_name="simulation_pret.pdf", mime="application/pdf")
st.markdown("### 💱 Besoin de convertir en une autre devise ?")
st.markdown(
    "[🔗 Accédez à notre convertisseur de devises ici](https://convertisseur-devises-kt5zgp7dgpw8dzkosvut75.streamlit.app/)",
    unsafe_allow_html=True
)
st.markdown("---")
st.markdown(
    "<div style='text-align: center; font-size: 14px;'>"
    "© 2025 - Crée  par <strong>Ibrahim DABRE </strong>"
    "</div>",
    unsafe_allow_html=True
)
