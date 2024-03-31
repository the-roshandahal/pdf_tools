from django.urls import path
from . import views

urlpatterns = [
    path('add_pdf/', views.add_pdf, name='add_pdf'),
    path('read/<int:pdf_id>/', views.read_pdf, name='read_pdf'),
]
