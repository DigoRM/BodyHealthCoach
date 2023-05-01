from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    path('minha_evolucao/', views.minha_evolucao, name='minha_evolucao'),
    path('aluno/<int:pk>/evolucao/', views.evolucao_do_aluno, name='evolucao_do_aluno'),
    path('evolucao_coach/', views.evolucao_coach, name='evolucao_coach'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)