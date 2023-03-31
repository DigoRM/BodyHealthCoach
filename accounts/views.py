from collections import defaultdict
import datetime
import json
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractDay, ExtractWeek
from datetime import datetime
from django.http import Http404
from matplotlib.pyplot import get
from .decorators import staff_required


from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts.forms import CreateUserForm
from .models import Aluno, Coach, Protocolo, Feedback, Retorno, Replica
from .forms import PerfilAluno, GerenciarAluno, NovoFeedback, NovoProtocolo, NovoRetorno, PerfilCoach, NovaReplica

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

from datetime import timedelta
from django.utils import timezone
def home(request):
    if request.user.is_authenticated:
        user = request.user
        if hasattr(user, 'coach'):
            coach = user.coach
            todos_alunos = Aluno.objects.filter(coach=coach).order_by('-cadastrado_em')
            alunos_ativos = Aluno.objects.filter(pago=True,coach=coach).order_by('-cadastrado_em')
            alunos_inativos = Aluno.objects.filter(pago=False,coach=coach).order_by('-cadastrado_em')
            alunos_novos = Aluno.objects.filter(coach__isnull=True).order_by('-cadastrado_em')
            
            today = date.today()
            vencimento = today + timedelta(days=7)
            alunos_expirando = Aluno.objects.filter(
                pago=True,
                coach=coach,
                vencimento_plano__range=[today, vencimento]
            ).order_by('-vencimento_plano')



            basic = Aluno.objects.filter(pago=True,coach=coach,plano=1).order_by('-cadastrado_em')
            silver = Aluno.objects.filter(pago=True,coach=coach,plano=2).order_by('-cadastrado_em')
            gold = Aluno.objects.filter(pago=True,coach=coach,plano=3).order_by('-cadastrado_em')
            atleta = Aluno.objects.filter(pago=True,coach=coach,plano=4).order_by('-cadastrado_em')


            feedbacks = Feedback.objects.filter(coach=coach, atendido=False)

            # Sum the mensalidade field of all active students
            receita = alunos_ativos.aggregate(Sum('mensalidade'))['mensalidade__sum'] or 0

            context = {
                'alunos_ativos':alunos_ativos,
                'alunos_inativos':alunos_inativos,
                'alunos_novos':alunos_novos,
                'user':user,
                'feedbacks':feedbacks,
                'todos_alunos':todos_alunos,
                'basic':basic,
                'silver':silver,
                'gold':gold,
                'atleta':atleta,
                'receita':receita,
                'alunos_expirando':alunos_expirando,
            }
            return render(request, 'home.html', context)

        elif hasattr(user, 'aluno'):
            aluno = user.aluno
            protocolos = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em')

            if protocolos.exists():
                protocolo_atual = protocolos[0]
            else:
                protocolo_atual = None

            # ultimo feedback
            feedbacks_atual = Feedback.objects.filter(protocolo=protocolo_atual).order_by('-cadastrado_em')
            if feedbacks_atual.exists():
                ultimo_feedback = feedbacks_atual[0]
            else:
                ultimo_feedback = None

            # ultimo retorno
            ultimo_retornos = Retorno.objects.filter(protocolo=protocolo_atual).order_by('-cadastrado_em')
            if ultimo_retornos.exists():
                ultimo_retorno = ultimo_retornos[0]
            else:
                ultimo_retorno = None
                
            feedbacks=[]
            for protocolo in protocolos:
                feedbacks += list(Protocolo.objects.filter(protocolo=protocolo))
            retornos = []
            for feedback in feedbacks:
                retornos += list(Retorno.objects.filter(feedback=feedback))

            today = timezone.now()
            next_feedback_date = None
            show_button = False
            if ultimo_feedback:
                next_feedback_date = ultimo_feedback.cadastrado_em + timedelta(days=1)
                show_button = next_feedback_date <= today
            elif protocolo_atual and ultimo_feedback is None:
                next_feedback_date = protocolo_atual.cadastrado_em + timedelta(days=1)
                show_button = next_feedback_date <= today




            context = {
                'user':user,
                'protocolos':protocolos,
                'feedbacks':feedbacks,
                'retornos':retornos,
                'aluno':aluno,
                'protocolo_atual':protocolo_atual,
                'ultimo_feedback':ultimo_feedback,
                'ultimo_retorno':ultimo_retorno,
                'next_feedback_date': next_feedback_date,
                'show_button':show_button,

            }
            return render(request, 'home.html', context)
    return render(request, 'home.html')


@staff_required
def todos_alunos(request):
    alunos_ativos = Aluno.objects.filter(pago=True).order_by('cadastrado_em')
    alunos_inativos = Aluno.objects.filter(pago=False).order_by('cadastrado_em')
    
    context = {
        'alunos_ativos':alunos_ativos,
        'alunos_inativos':alunos_inativos,
    }

    return render(request, 'coach/todos_alunos.html', context)


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


# Perfil Aluno e Coach 
@login_required(login_url='login')
def edit_profile(request, pk=None):
    user = request.user
    
    if hasattr(user, 'aluno'):
        aluno = user.aluno
        form = PerfilAluno(request.POST or None, request.FILES or None, instance=aluno)
        form2 = None
    elif hasattr(user, 'coach'):
        coach = user.coach
        form = None
        form2 = PerfilCoach(request.POST or None, request.FILES or None, instance=coach)
    else:
        raise Http404("This user is not an 'aluno' or a 'coach'.")
        
    if request.method == 'POST':
        if form and form.is_valid() or form2 and form2.is_valid():
            form.save() if form else form2.save()
            messages.success(request, 'Perfil Atualizado!')
            redirect_url = request.META.get('HTTP_REFERER', 'my_tasks')
            return redirect(redirect_url)
        else:
            print(form.errors if form else form2.errors)
            
    context = {
        'form': form,
        'form2': form2,

    }
    
    return render(request, 'alunos/edit_profile.html', context)

@staff_required
def perfil_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    protocolos = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em')

    if protocolos.exists():
        protocolo_atual = protocolos[0]
    else:
        protocolo_atual = None
    # ultimo feedback
    feedbacks_atual = Feedback.objects.filter(protocolo=protocolo_atual).order_by('-cadastrado_em')
    if feedbacks_atual.exists():
        ultimo_feedback = feedbacks_atual[0]
    else:
        ultimo_feedback = None
    # ultimo retorno
    ultimo_retornos = Retorno.objects.filter(protocolo=protocolo_atual).order_by('-cadastrado_em')
    if ultimo_retornos.exists():
        ultimo_retorno = ultimo_retornos[0]
    else:
        ultimo_retorno = None
        
    feedbacks=[]
    for protocolo in protocolos:
        feedbacks += list(Protocolo.objects.filter(protocolo=protocolo))
    retornos = []
    for feedback in feedbacks:
        retornos += list(Retorno.objects.filter(feedback=feedback))

    context = {
        'aluno':aluno,
        'protocolos':protocolos,
        'ultimo_feedback':ultimo_feedback,
        }

    return render(request, 'coach/perfil_aluno.html', context)

#Feedback
@login_required(login_url='login')
def novo_feedback(request):
    user = request.user
    aluno = user.aluno

    if request.method == 'POST':
        form = NovoFeedback(request.POST, request.FILES)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.aluno = aluno
            feedback.coach = aluno.coach
            feedback.save()
            messages.success(request, 'Feedback Enviado!')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = NovoFeedback()

    context = {
        'form': form,
        'aluno': aluno,
    }
    return render(request, 'alunos/novo_feedback.html', context)

@login_required(login_url='login')
def novo_feedbackV1(request, pk):
    user = request.user
    aluno = user.aluno
    protocolo = get_object_or_404(Protocolo,pk=pk)

    if request.method == 'POST':
        form = NovoFeedback(request.POST, request.FILES)

        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.aluno = aluno
            feedback.coach = aluno.coach
            feedback.protocolo = protocolo
            feedback.save()
            aluno.peso_atual = feedback.peso_atual
            aluno.save()
            messages.success(request, 'Feedback Enviado!')
            return redirect('meus_feedbacks')
        else:
            print(form.errors)
    else:
        form = NovoFeedback()

    context = {
        'form': form,
        'aluno': aluno,
        'protocolo':protocolo,
    }
    return render(request, 'alunos/novo_feedback.html', context)


@login_required
def meus_feedbacks(request):
    user = request.user
    try:
        feedbacks_aluno = Feedback.objects.filter(aluno=user.aluno)
    except Aluno.DoesNotExist:
        feedbacks_aluno = Feedback.objects.none()
    try:
        feedbacks_coach = Feedback.objects.filter(coach=user.coach)
    except Coach.DoesNotExist:
        feedbacks_coach = Feedback.objects.none()

    context = {'user': user,'feedbacks_aluno':feedbacks_aluno, 'feedbacks_coach':feedbacks_coach}
    
    return render(request, 'alunos/meus_feedbacks.html', context)

@staff_required
def feedbacks_pendentes(request):
    user = request.user
    coach = user.coach
    feedbacks = Feedback.objects.filter(coach=coach, atendido=False)
    retornos = []
    for feedback in feedbacks:
        retornos += list(Retorno.objects.filter(feedback=feedback))

    context = {'user': user,'coach':coach,'feedbacks':feedbacks,'retornos':retornos}
    
    return render(request, 'coach/feedbacks_pendentes.html', context)



@login_required
def feedback_detail(request, pk=None):
    feedback = get_object_or_404(Feedback, pk=pk)
    try:
        retorno = Retorno.objects.get(feedback=feedback)
    except Retorno.DoesNotExist:
        retorno = None    
    user = request.user
    
        
    context = {'feedback':feedback, 'retorno':retorno, 'user':user}
    
    return render(request, 'alunos/feedback_detail.html', context)

# Coach
@staff_required
def meus_alunos(request):
    user = request.user
    coach = user.coach
    alunos_ativos = Aluno.objects.filter(pago=True, coach=coach).order_by('-atualizado_em')
    
    context = {
        'alunos_ativos':alunos_ativos,
        'user':user,
    }

    return render(request, 'coach/meus_alunos.html', context)


from datetime import date, timedelta

@staff_required
def alunos_expirando(request):
    user = request.user
    coach = user.coach
    today = date.today()
    vencimento = today + timedelta(days=7)
    alunos_expirando = Aluno.objects.filter(
        pago=True,
        coach=coach,
        vencimento_plano__range=[today, vencimento]
    ).order_by('-vencimento_plano')

    context = {
        'alunos_expirando': alunos_expirando,
        'user': user,
    }

    return render(request, 'coach/alunos_expirando.html', context)

@staff_required
def novos_alunos(request):
    user = request.user
    novos_alunos = Aluno.objects.filter(coach__isnull=True).order_by('cadastrado_em')

    context = {
        'novos_alunos':novos_alunos,
        'user':user,
    }

    return render(request, 'coach/novos_alunos.html', context)


@staff_required
def gerenciar_aluno(request, pk=None):
    user = request.user
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = GerenciarAluno(request.POST, instance=aluno)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aluno atualizado!')
            return redirect('home')
        else:
            print(form.errors)
    else:
        form = GerenciarAluno(instance=aluno)
        
    context = {
        'form':form,
        'aluno':aluno,
        'user':user,
    }
    return render(request, 'coach/gerenciar_aluno.html',context)

# Protocolo
@staff_required
@login_required(login_url='login')
def novo_protocolo(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    user = request.user    
    if request.method == "POST":
        form = NovoProtocolo(request.POST, request.FILES)
        
        if form.is_valid():
            protocolo = form.save()
            protocolo.coach = user.coach
            protocolo.aluno = aluno
            protocolo.save()
            messages.success(request, 'Protocolo criado!')
            return redirect('meus_protocolos')
    else:
        form = NovoProtocolo()
        
    return render(request, 'coach/novo_protocolo.html', {'form':form, 'user':user, 'aluno':aluno,})

def meus_protocolos(request):
    user = request.user
    protocolos_aluno = Protocolo.objects.none()
    protocolos_coach = Protocolo.objects.none()

    if hasattr(user, 'aluno'):
        protocolos_aluno = Protocolo.objects.filter(aluno=user.aluno)
    
    if hasattr(user, 'coach'):
        protocolos_coach = Protocolo.objects.filter(coach=user.coach)

    context = {'user': user,'protocolos_coach':protocolos_coach, 'protocolos_aluno':protocolos_aluno}
    
    return render(request, 'alunos/meus_protocolos.html', context)


@login_required
def feedbacks_protocolo(request, pk):
    user = request.user
    protocolo = get_object_or_404(Protocolo, pk=pk)
    feedbacks = Feedback.objects.filter(protocolo=protocolo)
    retornos = []
    for feedback in feedbacks:
        retornos += list(Retorno.objects.filter(feedback=feedback))

    context = {'user': user,'feedbacks':feedbacks,'retornos':retornos, 'protocolo':protocolo}
    
    return render(request, 'alunos/feedbacks_protocolo.html', context)


@login_required(login_url='login')
def novo_retorno(request, pk):
    feedback = get_object_or_404(Feedback, pk=pk)
    #protocolo = get_object_or_404(Protocolo, feedback=feedback)
    user = request.user    
    if request.method == "POST":
        form2 = NovoRetorno(request.POST, request.FILES)
        
        if form2.is_valid():

            retorno = form2.save()
            retorno.feedback = feedback
            retorno.protocolo = feedback.protocolo
            retorno.save()
            feedback.atendido = True
            feedback.retorno = retorno
            feedback.save()

            messages.success(request, 'Retorno finalizado!')
            return redirect('feedbacks_pendentes')
    else:
        form2 = NovoRetorno()
        
    context = {'user':user, 'form2':form2,'feedback':feedback,}
    return render(request, 'coach/novo_retorno.html', context)


def meus_retornos(request):
    user = request.user
    retornos_aluno = Retorno.objects.filter(aluno=user.aluno)
    retornos_coach = Retorno.objects.filter(coach=user.coach)

    
    context = {'user': user,'retornos_coach':retornos_coach, 'retornos_aluno':retornos_aluno}
    
    return render(request, 'alunos/meus_retornos.html', context)

@login_required
def retorno_detail(request, pk=None):
    retorno = get_object_or_404(Retorno, pk=pk)
    replicas = Replica.objects.filter(retorno=retorno)
    user = request.user
    
        
    context = {'replicas':replicas, 'retorno':retorno, 'user':user}
    
    return render(request, 'alunos/retorno_detail.html', context)

@login_required
def nova_replica(request, pk=None):
    retorno = get_object_or_404(Retorno, pk=pk)
    replicas = Replica.objects.filter(retorno=retorno)
    user = request.user

    if request.method == 'POST':
        form = NovaReplica(request.POST)

        if form.is_valid():
            replica = form.save(commit=False)
            replica.author = user
            replica.save()
            messages.success(request, 'Enviado!')
            return redirect('feedbacks_pendentes')
        else:
            print(form.errors)
    else:
        form = NovaReplica()

    
        
    context = {'replicas':replicas, 'retorno':retorno, 'user':user, 'form':form,}
    
    return render(request, 'alunos/nova_replica.html', context)