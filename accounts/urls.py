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
    
    path("", views.home, name='home'),
    path('aluno/<int:pk>/aluno_pagou/', views.marcar_pago, name='marcar_pago'),
    path('aluno/<int:pk>/aluno_nao_pagou/', views.desmarcar_pago, name='desmarcar_pago'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)