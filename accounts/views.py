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

from accounts.utils import detectUser
from .decorators import staff_required


from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

from accounts.forms import CreateUserForm
from .models import Aluno, Coach, Protocolo, Feedback, Retorno, Replica
from .forms import PerfilAluno, GerenciarAluno, NovoFeedback, NovoProtocolo, NovoRetorno, PerfilCoach, NovaReplica
from django.core.mail import send_mail
from django.conf import settings

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
            feedbacks_aluno = Feedback.objects.filter(aluno=aluno).order_by('-cadastrado_em')
            if feedbacks_aluno.exists():
                ultimo_feedback_aluno = feedbacks_aluno[0]
            else:
                ultimo_feedback_aluno = None

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
                next_feedback_date = ultimo_feedback.cadastrado_em + timedelta(days=14)
                show_button = next_feedback_date <= today
            elif protocolo_atual and ultimo_feedback is None:
                next_feedback_date = protocolo_atual.cadastrado_em + timedelta(days=14)
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
                'ultimo_feedback_aluno':ultimo_feedback_aluno,

            }
            return render(request, 'home.html', context)
    return render(request, 'home.html')


@staff_required
def dashboard_coach(request):
    user= request.user
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
    return render(request, 'coach/dashboard.html', context)

@staff_required
def dashboard_aluno(request):
    user= request.user
    aluno = user.aluno
    protocolos = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em')
    feedbacks_aluno = Feedback.objects.filter(aluno=aluno).order_by('-cadastrado_em')
    if feedbacks_aluno.exists():
        ultimo_feedback_aluno = feedbacks_aluno[0]
    else:
        ultimo_feedback_aluno = None
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
        'ultimo_feedback_aluno':ultimo_feedback_aluno,
    }
    return render(request, 'alunos/dashboard.html', context)



@staff_required
def todos_alunos(request):
    alunos_ativos = Aluno.objects.filter(pago=True).order_by('vencimento_plano')
    alunos_inativos = Aluno.objects.filter(pago=False).order_by('vencimento_plano')
    today = date.today()
    
    
    context = {
        'alunos_ativos':alunos_ativos,
        'alunos_inativos':alunos_inativos,
        'today':today,
    }

    return render(request, 'coach/todos_alunos.html', context)

@staff_required
def marcar_pago(request, pk):
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.pago = True
    aluno.save()
    messages.success(request, 'Aluno pagou!')


    return redirect(redirect_url)

@staff_required
def desmarcar_pago_em_massa(request):
    coach = request.user.coach
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    today = date.today()
    expired_planos = Aluno.objects.filter(pago=True, vencimento_plano__lte=today, coach=coach)
    count = expired_planos.count()
    for aluno in expired_planos:
        aluno.pago = False
        aluno.save()
    messages.warning(request, f'{count} alunos marcados como não pagos.')


    return redirect(redirect_url)

from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

@staff_required
def avisar_alunos_novo_feedback(request):
    coach = request.user.coach
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    today = timezone.now().date()

    # Get all the paid students
    alunos = Aluno.objects.filter(pago=True, coach=coach)

    count = 0  # Initialize the count variable to 0

    # Loop through the students
    for aluno in alunos:
        # Get the last protocolo of the student
        last_protocolo = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em').first()
        # Get the last feedback of the student
        last_feedback = Feedback.objects.filter(aluno=aluno).order_by('-cadastrado_em').first()
        
        # If there is no feedback for this student, send an email if it has been 15 days since the last protocolo
        if not last_feedback and last_protocolo and last_protocolo.cadastrado_em.date() <= today - timedelta(days=15):
            subject = 'Lembrete para enviar feedback'
            message = f'Olá {aluno.nome},\n\nVocê ainda não enviou o feedback referente ao protocolo {last_protocolo.cadastrado_em}. Por favor, envie o feedback o mais breve possível.\n\nObrigado!'
            from_email = 'your_email@example.com'
            recipient_list = [aluno.email]
            send_mail(subject, message, from_email, recipient_list)
            count += 1  # Increment the count variable
        
        # If there is a feedback for this student, send an email if it has been 15 days since the last feedback
        elif last_feedback and last_feedback.cadastrado_em.date() <= today - timedelta(days=15):
            subject = 'Lembrete para enviar feedback'
            message = f'Olá {aluno.nome},\n\nVocê ainda não enviou o feedback referente ao protocolo {last_feedback.protocolo.cadastrado_em}. Por favor, envie o feedback o mais breve possível.\n\nObrigado!'
            from_email = 'your_email@example.com'
            recipient_list = [aluno.email]
            send_mail(subject, message, from_email, recipient_list)
            count += 1  # Increment the count variable

    messages.warning(request, f'{count} emails de lembrete enviados para os alunos.')

    return redirect(redirect_url)


def desmarcar_pago(request, pk):
    redirect_url = request.META.get('HTTP_REFERER', 'home')
    aluno = get_object_or_404(Aluno, pk=pk)
    aluno.pago = False
    aluno.save()
    messages.warning(request, 'Aluno não pagou! ')


    return redirect(redirect_url)

from PIL import Image, ExifTags
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile

def resize_image(image):
    if not image:
        return None

    # Check if uploaded file is PNG
    if image.name.endswith('.png'):
        # Open PNG image and convert to RGB format
        img = Image.open(image)
        img = img.convert('RGB')
    else:
        img = Image.open(image)

    # Get exif orientation
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(img._getexif().items())
        if exif[orientation] == 3:
            img = img.rotate(180, expand=True)
        elif exif[orientation] == 6:
            img = img.rotate(270, expand=True)
        elif exif[orientation] == 8:
            img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        # If there is no exif information, do nothing
        pass

    # Resize image
    img = img.resize((550, 650), Image.ANTIALIAS)

    # Save image to memory buffer as JPEG
    buffer = BytesIO()
    img.save(buffer, format='JPEG', quality=85)
    buffer.seek(0)

    # Determine content type of saved image
    content_type = 'image/jpeg'
    if image.name.endswith('.png'):
        content_type = 'image/png'

    return InMemoryUploadedFile(buffer, None, image.name, content_type,
                                buffer.getbuffer().nbytes, None)




# Perfil Aluno e Coach 
@login_required(login_url='login')
def edit_profile(request, pk=None):
    user = request.user
    
    if hasattr(user, 'aluno'):
        aluno = user.aluno
        form = PerfilAluno(request.POST or None, request.FILES or None, instance=aluno)
        form2 = None
        instance = aluno  # set instance to aluno if user is an 'aluno'
    elif hasattr(user, 'coach'):
        coach = user.coach
        form = None
        form2 = PerfilCoach(request.POST or None, request.FILES or None, instance=coach)
        instance = coach  # set instance to coach if user is a 'coach'
    else:
        raise Http404("This user is not an 'aluno' or a 'coach'.")
        
    image_fields = ['avatar', 'foto_frente', 'foto_lado', 'foto_verso']

    if request.method == 'POST':
        if form and form.is_valid() or form2 and form2.is_valid():
            # Loop through image fields and resize uploaded images
            for field in image_fields:
                if request.FILES.get(field):
                    image = request.FILES[field]
                    image_file = resize_image(image)
                    setattr(instance, field, image_file)
            
            # Save the form
            if form is not None:
                form.save()
            elif form2 is not None:
                form2.save()
            
            messages.success(request, 'Perfil Atualizado!')
            return redirect('home')
        else:
            messages.warning(request,form.errors if form else form2.errors)
            
    context = {
        'form': form,
        'form2': form2,
    }
    
    return render(request, 'alunos/edit_profile.html', context)


@staff_required
def perfil_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    protocolos = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em')
    feedbacks = Feedback.objects.filter(aluno=aluno).order_by('-cadastrado_em')

    if protocolos.exists():
        protocolo_atual = protocolos[0]
    else:
        protocolo_atual = None

    if feedbacks.exists():
        ultimo_feedback_aluno = feedbacks[0]
    else:
        ultimo_feedback_aluno = None
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
        'ultimo_feedback_aluno':ultimo_feedback_aluno,
        'feedbacks':feedbacks,
        }

    return render(request, 'coach/perfil_aluno.html', context)

@staff_required
def exames_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    feedbacks = Feedback.objects.filter(aluno=aluno, exame_sangue__isnull=False).order_by('-cadastrado_em')

    context = {
        'aluno':aluno,
        'feedbacks':feedbacks,
        }

    return render(request, 'coach/exames_aluno.html', context)

@login_required
def meus_exames(request):
    aluno = request.user.aluno
    feedbacks = Feedback.objects.filter(aluno=aluno, exame_sangue__isnull=False).order_by('-cadastrado_em')

    context = {
        'aluno':aluno,
        'feedbacks':feedbacks,
        }

    return render(request, 'alunos/meus_exames.html', context)

@staff_required
def avaliacoes_fisicas_aluno(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    feedbacks = Feedback.objects.filter(aluno=aluno, avaliacao_fisica__isnull=False).order_by('-cadastrado_em')

    context = {
        'aluno':aluno,
        'feedbacks':feedbacks,
        }

    return render(request, 'coach/avaliacoes_fisicas_aluno.html', context)

@login_required
def avaliacoes_fisicas(request):
    aluno = request.user.aluno
    feedbacks = Feedback.objects.filter(aluno=aluno, avaliacao_fisica__isnull=False).order_by('-cadastrado_em')

    context = {
        'aluno':aluno,
        'feedbacks':feedbacks,
        }

    return render(request, 'alunos/avaliacoes_fisicas.html', context)



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

            # Resize images
            if feedback.foto_frente:
                feedback.foto_frente = resize_image(feedback.foto_frente)
            if feedback.foto_lado:
                feedback.foto_lado = resize_image(feedback.foto_lado)
            if feedback.foto_verso:
                feedback.foto_verso = resize_image(feedback.foto_verso)

            feedback.save()
            aluno.peso_atual = feedback.peso_atual
            aluno.save()

            subject = 'Novo Feedback Recebido'
            message = f'Olá {feedback.coach.nome},\n\nUm feedback foi enviado para você! https://sennateam.up.railway.app/feedbacks_pendentes/'
            from_email = 'rmarcolino.consultoria@gmail.com'
            recipient_list = [feedback.coach.email]
            send_mail(subject, message, from_email, recipient_list)
            
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
def planos_expirados(request):
    user = request.user
    coach = user.coach
    today = date.today()
    planos_expirados = Aluno.objects.filter(
        pago=True,
        coach=coach,
        vencimento_plano__lt=today
    ).order_by('-vencimento_plano')

    context = {
        'planos_expirados': planos_expirados,
        'user': user,
    }

    return render(request, 'coach/planos_expirados.html', context)



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
    coach = user.coach
    aluno = get_object_or_404(Aluno, pk=pk)
    if request.method == 'POST':
        form = GerenciarAluno(request.POST, instance=aluno)
        if form.is_valid():
            aluno = form.save()
            aluno.coach = coach
            aluno.pago = True
            aluno.save()
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
def novo_protocolo(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    user = request.user    
    if request.method == "POST":
        form = NovoProtocolo(request.POST, request.FILES)
        
        if form.is_valid():
            protocolo = form.save()
            protocolo.coach = user.coach
            protocolo.aluno = aluno
            protocolo.kcal = (protocolo.prot*4)+(protocolo.carbo*4)+(protocolo.fat*9)
            protocolo.save()
            subject = 'Novo Protocolo Recebido'
            message = f'Olá {aluno.nome},\n\nUm protocolo foi enviado para você! https://sennateam.up.railway.app/'
            from_email = 'rmarcolino.consultoria@gmail.com'
            recipient_list = [aluno.email]
            send_mail(subject, message, from_email, recipient_list)


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
        protocolos_aluno = Protocolo.objects.filter(aluno=user.aluno).order_by('-cadastrado_em')

    if hasattr(user, 'coach'):
        alunos = Aluno.objects.filter(coach=user.coach,pago=True).order_by('nome')
        protocolos_coach = []
        for aluno in alunos:
            protocolos_aluno = Protocolo.objects.filter(aluno=aluno).order_by('-cadastrado_em')
            protocolos_coach.append({'aluno': aluno, 'protocolos_aluno': protocolos_aluno})

        print(protocolos_coach)

    context = {'user': user,'protocolos_coach':protocolos_coach, 'protocolos_aluno':protocolos_aluno,}
    
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
            retorno.aluno = feedback.aluno
            retorno.coach = feedback.coach
            retorno.save()
            feedback.atendido = True
            feedback.retorno = retorno
            feedback.save()

            subject = 'Novo Retorno Recebido'
            message = f'Olá {retorno.aluno.nome},\n\nUm retorno foi enviado para você! https://sennateam.up.railway.app/'
            from_email = 'rmarcolino.consultoria@gmail.com'
            recipient_list = [retorno.aluno.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Retorno finalizado!')
            return redirect('feedbacks_pendentes')
    else:
        form2 = NovoRetorno()
        
    context = {'user':user, 'form2':form2,'feedback':feedback,}
    return render(request, 'coach/novo_retorno.html', context)


@login_required
def meus_retornos(request):
    user = request.user
    retornos_aluno = Retorno.objects.none()
    retornos_coach = Retorno.objects.none()

    if hasattr(user, 'aluno'):
        retornos_aluno = Retorno.objects.filter(aluno=user.aluno).order_by('-cadastrado_em')

    if hasattr(user, 'coach'):
        alunos = Aluno.objects.filter(coach=user.coach,pago=True).order_by('nome')
        retornos_coach = []
        for aluno in alunos:
            retornos_aluno = Retorno.objects.filter(aluno=aluno).order_by('-cadastrado_em')
            retornos_coach.append({'aluno': aluno, 'retornos_aluno': retornos_aluno})


    
    context = {'user': user,'retornos_coach':retornos_coach, 'retornos_aluno':retornos_aluno}
    
    return render(request, 'alunos/meus_retornos.html', context)



from django.db.models import Count

@staff_required
def retornos_com_replica(request):
    user = request.user
    coach = user.coach
    retornos = Retorno.objects.filter(coach=coach).annotate(num_replicas=Count('replica'))
    retornos_com_replica = retornos.filter(num_replicas=1)
    

    context = {'user': user, 'retornos_com_replica': retornos_com_replica}
    return render(request, 'coach/retornos_com_replica.html', context)



@login_required
def retorno_detail(request, pk=None):
    retorno = get_object_or_404(Retorno, pk=pk)
    replicas = Replica.objects.filter(retorno=retorno)
    limite_replicas = replicas.count() < 2
    user = request.user

    if request.method == "POST":
        form = NovaReplica(request.POST, request.FILES)
        
        if form.is_valid():

            replica = form.save()
            replica.author = user
            replica.retorno=retorno
            replica.save()
            retorno.replica = replica
            retorno.save()

            subject = 'Nova Réplica Recebida'
            message = f'Olá {replica.author.username},\n\nUma réplica foi enviada para você! https://sennateam.up.railway.app/'
            from_email = 'rmarcolino.consultoria@gmail.com'
            recipient_list = [replica.author.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Réplica enviada!')
            redirect_url = request.META.get('HTTP_REFERER', 'my_tasks')
            return redirect(redirect_url)
    else:
        form = NovaReplica()
    
        
    context = {'replicas':replicas, 'retorno':retorno, 'user':user ,'form':form, 'limite_replicas':limite_replicas,}
    
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
            retorno.replica = replica
            retorno.save()

            subject = 'Nova Réplica Recebida'
            message = f'Olá {replica.author.username},\n\nUma réplica foi enviada para você! https://sennateam.up.railway.app/'
            from_email = 'rmarcolino.consultoria@gmail.com'
            recipient_list = [replica.author.email]
            send_mail(subject, message, from_email, recipient_list)

            messages.success(request, 'Enviado!')
            return redirect('feedbacks_pendentes')
        else:
            print(form.errors)
    else:
        form = NovaReplica()

    
        
    context = {'replicas':replicas, 'retorno':retorno, 'user':user, 'form':form,}
    
    return render(request, 'alunos/nova_replica.html', context)