import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from io import BytesIO

load_dotenv()

def add_image_to_pdf(input_pdf_path, output_pdf_path, image_path):
    # Configurações críticas
    LEFT_COLUMN_WIDTH = 170  # Largura exata da coluna do LinkedIn (em pontos)
    BACKGROUND_COLOR = HexColor("#607d8b")
    IMG_SIZE = 100  # Tamanho padrão para foto em CVs
    IMG_X = 40  # Margem esquerda
    IMG_Y = 680  # Posição vertical (ajuste conforme seu PDF)

    # Passo 1: Criar uma camada de fundo
    background = BytesIO()
    c = canvas.Canvas(background, pagesize=A4)
    
    # Desenha o fundo colorido
    c.setFillColor(BACKGROUND_COLOR)
    c.rect(0, 0, LEFT_COLUMN_WIDTH, A4[1], fill=1)  # Preenche toda a altura
    
    # Adiciona a imagem (PNG com transparência)
    c.drawImage(image_path, IMG_X, IMG_Y, IMG_SIZE, IMG_SIZE, mask='auto')
    c.save()
    background.seek(0)

    # Passo 2: Mesclar camadas (fundo + original)
    original = PdfReader(input_pdf_path)
    page = original.pages[0]
    
    # Mescla o fundo por BAIXO do conteúdo existente
    page.merge_page(PdfReader(background).pages[0], over=False)  # <--- Key Fix
    
    # Passo 3: Salvar o PDF modificado
    writer = PdfWriter()
    writer.add_page(page)
    with open(output_pdf_path, "wb") as f:
        writer.write(f)

def main():
    # Carrega caminhos do .env
    input_pt = os.getenv("PDF_INPUT_PATH_PT-BR")
    output_pt = os.getenv("PDF_OUTPUT_PATH_PT-BR")
    img_path = os.getenv("IMG_PATH")

    # Processa apenas um arquivo para teste
    add_image_to_pdf(input_pt, output_pt, img_path)
    print("PDF modificado com sucesso!")

if __name__ == "__main__":
    main()