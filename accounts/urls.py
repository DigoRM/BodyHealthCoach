from django.urls import path, include
from . import views
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView,PasswordResetCompleteView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    #Registration/Login/Logout/Password
    path('reset_password/', PasswordResetView.as_view(), name='reset_password'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('reset_password_done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    path("", views.home, name='home'),
    path('meus_alunos/', views.meus_alunos, name='meus_alunos'),
    path('novos_alunos/', views.novos_alunos, name='novos_alunos'),


    path('aluno/<int:pk>/aluno_pagou/', views.marcar_pago, name='marcar_pago'),
    path('aluno/<int:pk>/aluno_nao_pagou/', views.desmarcar_pago, name='desmarcar_pago'),
    path('novo_feedback/', views.novo_feedback, name='novo_feedback'),
    path('novo/<int:pk>/feedback/', views.novo_feedbackV1, name='novo_feedbackV1'),

    path('meus_feedbacks/', views.meus_feedbacks, name='meus_feedbacks'),
    path('feedbacks_pendentes/', views.feedbacks_pendentes, name='feedbacks_pendentes'),

    path('feedback/<int:pk>/detail/', views.feedback_detail, name='feedback_detail'),
    path('aluno/<int:pk>/gerenciar/', views.gerenciar_aluno, name='gerenciar_aluno'),
    path('protocolo/<int:pk>/novo/', views.novo_protocolo, name='novo_protocolo'),
    path('meus_protocolos/', views.meus_protocolos, name='meus_protocolos'),

    path('retorno/<int:pk>/novo/', views.novo_retorno, name='novo_retorno'),

    path('meus_retornos/', views.meus_retornos, name='meus_retornos'),
    path('retorno/<int:pk>/detail/', views.retorno_detail, name='retorno_detail'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)