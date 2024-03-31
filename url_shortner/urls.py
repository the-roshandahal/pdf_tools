from django.urls import path
from . import views
from django.urls import re_path
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static  


urlpatterns = [
    path('shorten_url', views.shorten_url, name='shorten_url'),
    path('su/<str:short_url>', views.su, name='su'),
    path('<str:short_url>/', views.redirect_to_long_url, name='redirect_to_long_url'),

    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
