from fpdf import FPDF
import os

class MonPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Ajout de la police Unicode DejaVu
        self.add_font("DejaVu", "", os.path.join("fonts", "DejaVuSans.ttf"), uni=True)
        self.add_font("DejaVu", "B", os.path.join("fonts", "DejaVuSans-Bold.ttf"), uni=True)
        self.set_font("DejaVu", size=12)

    def header(self):
        self.set_font("DejaVu", "B", 16)
        self.cell(0, 10, "Rapport de simulation de prêt bancaire", ln=True, align="C")
        self.ln(10)

    def add_resume(self, resume_dict):
        self.set_fill_color(240, 240, 240)
        self.set_font("DejaVu", "B", 13)
        self.cell(0, 10, "Résumé du prêt", ln=True)
        self.set_font("DejaVu", size=11)
        self.ln(2)

        for label, value in resume_dict.items():
            self.set_fill_color(245, 245, 245)
            self.cell(90, 10, str(label), border=0, fill=True)
            self.cell(0, 10, str(value), ln=True)
        self.ln(5)

    def add_amortissement(self, df):
        self.set_font("DejaVu", "B", 13)
        self.cell(0, 10, "Tableau d'amortissement", ln=True)
        self.set_font("DejaVu", size=10)
        self.ln(2)

        col_widths = [20, 35, 35, 45, 50]
        headers = list(df.columns)

        self.set_fill_color(200, 200, 200)
        for i, col in enumerate(headers):
            self.cell(col_widths[i], 8, col, border=1, align="C", fill=True)
        self.ln()

        self.set_fill_color(255, 255, 255)
        for _, row in df.iterrows():
            for i, value in enumerate(row):
                self.cell(col_widths[i], 8, str(round(value, 2)), border=1, align="C")
            self.ln()

def generer_pdf(resume_dict, df_amort):
    pdf = MonPDF()
    pdf.add_page()
    pdf.add_resume(resume_dict)
    pdf.add_amortissement(df_amort)
    return bytes(pdf.output(dest="S"))  # ✅ correct pour Streamlit
