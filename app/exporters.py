import os
import time
from fpdf import FPDF

class ComicPDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'ComicCraft - AI Generated Comic', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

def save_pdf(comic_layout: list, story_title: str = "My Comic") -> str:
    os.makedirs("static/exports", exist_ok=True)
    pdf = ComicPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    for panel in comic_layout:
        pdf.add_page()
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Panel {panel['panel_number']}: {panel['title']}", 0, 1, 'L')
        img_relative_path = panel['image_path'].lstrip('/')
        if os.path.exists(img_relative_path):
            pdf.image(img_relative_path, x=25, y=30, w=160)
            pdf.ln(115)
        else:
            pdf.ln(10)
        pdf.set_font("Arial", "I", 10)
        pdf.multi_cell(0, 6, f"Scene: {panel['scene_description']}")
        pdf.ln(4)
        pdf.set_font("Arial", "", 11)
        pdf.multi_cell(0, 6, panel['story_text'])
    filename = f"comic_{int(time.time())}.pdf"
    output_path = os.path.join("static", "exports", filename)
    pdf.output(output_path)
    return f"/static/exports/{filename}"
