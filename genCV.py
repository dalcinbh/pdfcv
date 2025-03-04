import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO

load_dotenv()

def add_image_to_pdf(input_pdf_path, output_pdf_path, image_path):
    # Configurações principais
    BACKGROUND_COLOR = HexColor("#607d8b")
    COLUNA_ESQUERDA_LARGURA = A4[0] * 0.3  # 30% da largura
    IMG_WIDTH, IMG_HEIGHT = 120, 120
    IMG_X, IMG_Y = 20, A4[1] - 200  # Ajuste vertical para evitar texto

    # Passo 1: Cria uma camada de fundo com a cor desejada
    background_layer = BytesIO()
    can = canvas.Canvas(background_layer, pagesize=A4)
    can.setFillColor(BACKGROUND_COLOR)
    can.rect(0, 0, COLUNA_ESQUERDA_LARGURA, A4[1], fill=1)
    can.drawImage(image_path, IMG_X, IMG_Y, IMG_WIDTH, IMG_HEIGHT, mask='auto')
    can.save()
    background_layer.seek(0)

    # Passo 2: Mescla as camadas (fundo + PDF original)
    original_pdf = PdfReader(open(input_pdf_path, "rb"))
    background_pdf = PdfReader(background_layer)
    output = PdfWriter()

    # Mescla apenas na primeira página
    page = original_pdf.pages[0]
    page.merge_page(background_pdf.pages[0])
    output.add_page(page)

    # Adiciona páginas restantes (se houver)
    for page in original_pdf.pages[1:]:
        output.add_page(page)

    # Salva o PDF final
    with open(output_pdf_path, "wb") as f:
        output.write(f)

def main():
    # Carrega caminhos do .env
    pdf_input_pt = os.getenv("PDF_INPUT_PATH_PT-BR")
    pdf_output_pt = os.getenv("PDF_OUTPUT_PATH_PT-BR")
    img_path = os.getenv("IMG_PATH")

    # Processa o PDF (apenas em português para teste)
    add_image_to_pdf(pdf_input_pt, pdf_output_pt, img_path)
    print("PDF modificado com sucesso!")

if __name__ == "__main__":
    main()