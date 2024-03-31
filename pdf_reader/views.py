from django.shortcuts import render, redirect
from django.conf import settings
import PyPDF2
import pyttsx3
import os

from .models import PDFDocument

def add_pdf(request):
    if request.method == 'POST':
        # Handle file upload
        document = request.FILES.get('document')
        if document:
            pdf_document = PDFDocument.objects.create(document=document)
            return redirect('read_pdf', pdf_document.id)
    return render(request, 'add_pdf.html')

def read_pdf(request, pdf_id):
    pdf_document = PDFDocument.objects.get(pk=pdf_id)
    pdf_path = settings.MEDIA_ROOT + '/' + str(pdf_document.document)
    
    # Extract text from PDF
    pdf_text = extract_text_from_pdf(pdf_path)

    # Generate audio
    generate_audio(pdf_text)

    return render(request, 'read_pdf.html', {'pdf_text': pdf_text})



from PyPDF2 import PdfReader

import re

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            # Replace common bullet characters with a standard bullet character
            cleaned_text = re.sub(r'[\u2022\u2023\u2043\u25AA\u25CF\u25CB\u25E6]', '•', page_text)
            text += cleaned_text
    return text


import os
from django.conf import settings

def generate_audio(text, output_file='output.mp3'):
    # Determine the path to the media folder
    media_path = os.path.join(settings.MEDIA_ROOT, 'output')

    # Ensure that the output directory exists
    os.makedirs(media_path, exist_ok=True)

    # Determine the full path to the output file
    output_path = os.path.join(media_path, output_file)

    # Function to generate audio from text
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()

    # Return the relative path to the generated audio file
    return os.path.join('output', output_file)

