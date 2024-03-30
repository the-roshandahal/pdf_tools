import pypdfium2 as pdfium
from PIL import Image
import os
from io import BytesIO


def convert_pdf_to_images(pdf_file, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf = pdfium.PdfDocument(BytesIO(pdf_file.read()))
    for i in range(len(pdf)):
        page = pdf[i]
        image = page.render(scale=4).to_pil()
        image.save(os.path.join(output_dir, f"page_{i + 1}.jpg"))