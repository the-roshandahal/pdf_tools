from django.shortcuts import render, redirect
from .models import *
from .utils import convert_pdf_to_images
from django.conf import settings
import os

def home(request):
    return render(request, 'home.html')

def upload_pdf(request):
    if request.method == 'POST' and request.FILES.get('pdf_file'):
        pdf_file = request.FILES['pdf_file']
        output_dir = os.path.join(settings.MEDIA_ROOT, 'pdf_images')
        convert_pdf_to_images(pdf_file, output_dir)
        
        uploaded_pdf = UploadedPDF.objects.create(pdf_file=pdf_file)
        
        for image_filename in os.listdir(output_dir):
            image_path = os.path.join(output_dir, image_filename)
            ConvertedImage.objects.create(pdf=uploaded_pdf, image=image_path)
        
        return redirect('pdf_detail', id=uploaded_pdf.id)
    
    return render(request, 'upload_pdf.html')

def pdf_detail(request, id):
    try:
        pdf = UploadedPDF.objects.get(id=id)
        images = ConvertedImage.objects.filter(pdf=pdf)
        return render(request, 'pdf_detail.html', {'pdf': pdf, 'images': images})
    except UploadedPDF.DoesNotExist:
        return redirect('home')
