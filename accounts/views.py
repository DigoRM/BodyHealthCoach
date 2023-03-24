from collections import defaultdict
import datetime
import json
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractDay, ExtractWeek
from datetime import datetime

from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts.forms import CreateUserForm
from .models import Aluno, Coach

# Create Aluno or Coach Model based on Users Attribute:
def create_user_and_associated_object(username, password, is_staff, **kwargs):
    # Create a new user
    new_user = User.objects.create_user(username=username, password=password)

    # Create an associated Aluno or Coach object based on the user's attributes
    if is_staff:
        coach = Coach.objects.create(user=new_user, **kwargs)
        coach.save()
        return coach
    else:
        aluno = Aluno.objects.create(user=new_user, **kwargs)
        aluno.save()
        return aluno

#Login/Register/Logout/Password
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect.')
    return render(request, 'registration/login.html')    

def logoutUser(request):
    logout(request)
    return redirect('login')       


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')

                messages.success(request, "Welcome " + username + "!")
                
                
                return redirect('login')
        
        
        context = {
            'form':form,
                   }
        
        return render(request, 'registration/register.html', context)
    
def home(request):
    alunos_ativos = Aluno.objects.filter(pago=True).order_by('-atualizado_em')
    alunos_inativos = Aluno.objects.filter(pago=False).order_by('-atualizado_em')
    
    context = {
        'alunos_ativos':alunos_ativos,
        'alunos_inativos':alunos_inativos,
    }

    return render(request, 'home.html', context)


def marcar_pago(request, pk):
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.pago = True
    aluno.save()
    messages.success(request, 'Aluno pagou!')


    return redirect(redirect_url)

def desmarcar_pago(request, pk):
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.pago = False
    aluno.save()
    messages.warning(request, 'Aluno não pagou! ')


    return redirect(redirect_url)