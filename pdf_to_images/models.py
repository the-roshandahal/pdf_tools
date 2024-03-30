# pdf_converter/models.py
from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='pdf_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.pdf_file.name

class ConvertedImage(models.Model):
    pdf = models.ForeignKey(UploadedPDF, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='converted_images/')
