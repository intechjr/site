from django.conf import settings  # Importando settings
from django.conf.urls.static import static  # Importando para servir arquivos estáticos
from django.urls import path
from . import views  # Importa suas views

urlpatterns = [
    path('', views.home, name='base'),  # Sua URL principal
]

# Se estiver no modo DEBUG, serve arquivos de mídia
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
