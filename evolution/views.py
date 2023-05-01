from collections import defaultdict
import datetime
import json
from django.db.models import Count
from django.db.models import Q
from django.db.models import Sum
from decimal import Decimal
from django.db.models.functions import ExtractWeekDay, ExtractMonth, ExtractDay, ExtractWeek
from datetime import date, datetime
from django.http import Http404

from accounts.utils import detectUser
from accounts.decorators import staff_required
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import Aluno, Coach, Protocolo, Feedback, Retorno, Replica
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

@staff_required
def evolucao_coach(request):
    user = request.user
    coach = user.coach
    todos_alunos = Aluno.objects.filter(coach=coach).order_by('-cadastrado_em')
    alunos_ativos = Aluno.objects.filter(pago=True,coach=coach).order_by('-cadastrado_em')
    alunos_inativos = Aluno.objects.filter(pago=False,coach=coach).order_by('-cadastrado_em')
    alunos_novos = Aluno.objects.filter(coach__isnull=True).order_by('-cadastrado_em')
    
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

        'receita':receita,
    }
    return render(request, 'evolucao_coach.html', context)

# Reports
import plotly
import plotly.graph_objs as go

@login_required
def minha_evolucao(request):
    user = request.user
    aluno = user.aluno
    protocolos = Protocolo.objects.filter(aluno=aluno).order_by('cadastrado_em')
    feedbacks_aluno = Feedback.objects.filter(aluno=aluno).order_by('cadastrado_em')

    # Create data for the chart

    x = [protocolo.cadastrado_em for protocolo in protocolos]
    x2 = [feedback.cadastrado_em for feedback in feedbacks_aluno]
    x3 = aluno.cadastrado_em
    y = aluno.peso
    y1 = [feedback.peso_atual for feedback in feedbacks_aluno]
    y2 = [feedback.comprometimento for feedback in feedbacks_aluno]
    y3 = [feedback.avalia_coach for feedback in feedbacks_aluno]
    y4 = [protocolo.carbo for protocolo in protocolos]
    y5 = [protocolo.prot for protocolo in protocolos]
    y6 = [protocolo.fat for protocolo in protocolos]
    y7 = [protocolo.kcal for protocolo in protocolos]  
    y8 = [protocolo.treino for protocolo in protocolos]   

    # Create traces for the chart
    trace1 = go.Scatter(x=x2, y=y1, name='Peso atual', line=dict(width=2))
    trace2 = go.Scatter(x=[x3], y=[y], name='Peso Inicial', line=dict(width=2))
    trace_line = go.Scatter(x=[x2[0], x3], y=[y1[0], y], mode='lines', name='Peso Inicial até Peso atual')

    trace3 = go.Bar(x=x2, y=y2, name='Comprometimento')
    trace4 = go.Bar(x=x2, y=y3, name='Avaliação Consultoria')
    trace5 = go.Bar(x=x, y=y7, name='Kcal')

    pie_traces = []
    for protocolo in protocolos:
        pie_trace = go.Pie(labels=['Carbo', 'Prot', 'Fat'], 
                            values=[protocolo.carbo, protocolo.prot, protocolo.fat],
                            name=protocolo.treino, hole=0.5)
        pie_traces.append(pie_trace)

    # Create layout for the chart
    layout = go.Layout(title='Histórico Peso',
                    xaxis=dict(title='Data'),
                    yaxis=dict(title='Kg'))

    layout2 = go.Layout(title='Desempenho',
                    xaxis=dict(title='Data'),
                    yaxis=dict(title='Nota'))

    layout3 = go.Layout(title='Protocolos',
                    xaxis=dict(title='Data'),
                    yaxis=dict(title='Macros'))

    # Add traces and layout to the figure
    fig = go.Figure(data=[trace1, trace2, trace_line], layout=layout)
    fig2 = go.Figure(data=[trace3, trace4], layout=layout2)
    fig3 = go.Figure(data=[trace5, *pie_traces], layout=layout3)



    # Convert the figure to JSON so it can be rendered in the template
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    graphJSON3 = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)



    context = {
        'user': user,
        'protocolos': protocolos,
        'feedbacks_aluno': feedbacks_aluno,
        'aluno': aluno,
        'graphJSON': graphJSON,
        'graphJSON2': graphJSON2,
        'graphJSON3': graphJSON3,

    }

    return render(request, 'minha_evolucao.html', context)


@login_required
def evolucao_do_aluno(request, pk):
    user = request.user
    aluno = get_object_or_404(Aluno, pk)
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
        'feedbacks_aluno':feedbacks_aluno,
        'retornos':retornos,
        'aluno':aluno,
        'protocolo_atual':protocolo_atual,
        'ultimo_feedback':ultimo_feedback,
        'ultimo_retorno':ultimo_retorno,
        'next_feedback_date': next_feedback_date,
        'show_button':show_button,
        'ultimo_feedback_aluno':ultimo_feedback_aluno,
    }
    return render(request, 'evolucao_do_aluno.html', context)



