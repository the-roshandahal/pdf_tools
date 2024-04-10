from django.shortcuts import render, redirect
from django.conf import settings
from .models import PDFDocument
import os
import re
import PyPDF2
import pyttsx3

# This function handles the addition of a PDF document through a form submission.
# It checks if the request method is POST, then retrieves the uploaded document and creates a PDFDocument object.
# After creation, it redirects to the 'read_pdf' view passing the ID of the newly created PDFDocument.
def add_pdf(request):
    if request.method == 'POST':
        document = request.FILES.get('document')
        if document:
            pdf_document = PDFDocument.objects.create(document=document)
            return redirect('read_pdf', pdf_document.id)
    return render(request, 'add_pdf.html')


# This function extracts text from a PDF document along with timestamps for each word.
# It reads the PDF file page by page, extracts text, splits it into words, and assigns timestamps assuming 0.5 seconds per word.
def extract_text_with_timestamps(pdf_path):
    text_with_timestamps = []
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            word_list = page_text.split()
            start_time = 0
            for word in word_list:
                text_with_timestamps.append((word, start_time, start_time + 0.5))  # Assuming 0.5 seconds per word
                start_time += 0.5
    return text_with_timestamps
# This view retrieves a PDF document using its ID and extracts text with timestamps from it.
# It then renders the 'read_pdf.html' template with the extracted text as context.
def read_pdf(request, pdf_id):
    pdf_document = PDFDocument.objects.get(pk=pdf_id)
    pdf_path = os.path.join(settings.MEDIA_ROOT, str(pdf_document.document))
    pdf_text = extract_text_with_timestamps(pdf_path)
    return render(request, 'read_pdf.html', {'pdf_text': pdf_text})

# This function extracts text from a PDF document, replacing common bullet characters with a standard bullet character.
def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_num in range(len(pdf_reader.pages)):
            page_text = pdf_reader.pages[page_num].extract_text()
            cleaned_text = re.sub(r'[\u2022\u2023\u2043\u25AA\u25CF\u25CB\u25E6]', '•', page_text)
            text += cleaned_text
    return text


# This function generates audio from text and creates a file with timestamps for each word.
# It initializes a text-to-speech engine, saves audio to a file, and generates timestamps assuming 0.5 seconds per word.
def generate_audio_with_timestamps(text, output_file, timestamps_file):
    media_path = os.path.join(settings.MEDIA_ROOT, 'output')
    os.makedirs(media_path, exist_ok=True)
    output_path = os.path.join(media_path, output_file)
    timestamps_path = os.path.join(media_path, timestamps_file)
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    with open(timestamps_path, 'w', encoding='utf-8') as file:
        word_list = text.split()
        start_time = 0
        for word in word_list:
            file.write(f'{word} {start_time} {start_time + 0.5}\n')  # Assuming 0.5 seconds per word
            start_time += 0.5
