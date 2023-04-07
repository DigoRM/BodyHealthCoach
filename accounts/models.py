from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator



# Create your models here.


class Coach(models.Model):
    user = models.OneToOneField(User, related_name='coach', on_delete=models.CASCADE, blank=True,null=True)
    nome = models.CharField(max_length=255,blank=True, null=True)
    sobrenome = models.CharField(max_length=255,blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=255,blank=True, null=True)
    celular = models.CharField(max_length=33,blank=None,null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    altura = models.DecimalField(max_digits=2, decimal_places=2,blank=True, null=True)
    peso = models.DecimalField(max_digits=3, decimal_places=2,blank=True, null=True)
    conquistas = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='coach/foto_perfil',blank=True, null=True)
    foto_certificado = models.ImageField(upload_to='coach/certificado',blank=True, null=True)


    def __str__(self):
        return self.email



class Aluno(models.Model):

    BASIC = 1
    SILVER =2
    GOLD = 3
    ATLETA = 4
    
    CHOICE = (
        (BASIC, 'BASIC'),
        (SILVER, 'SILVER'),
        (GOLD, 'GOLD'),
        (ATLETA, 'ATLETA'),

    )

    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE, blank=True,null=True)
    coach = models.ForeignKey(Coach, related_name='aluno_coach', on_delete=models.CASCADE, blank=True,null=True)
    nome = models.CharField(max_length=255,blank=True, null=True)
    sobrenome = models.CharField(max_length=255,blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=255)
    celular = models.CharField(max_length=33,blank=True,null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    altura = models.DecimalField(max_digits=3, decimal_places=2,blank=True, null=True)
    peso = models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    peso_atual = models.DecimalField(max_digits=4, decimal_places=2,blank=True, null=True)
    enfermidades = models.CharField(max_length=255,blank=True, null=True)
    medicamentos = models.CharField(max_length=255,blank=True, null=True)
    lesao = models.CharField(max_length=255,blank=True, null=True)
    objetivo_curto = models.CharField(max_length=155)
    objetivo_longo = models.CharField(max_length=155)
    avatar = models.ImageField(upload_to='alunos/avatar',blank=True, null=True)
    foto_frente = models.ImageField(upload_to='alunos/foto_frente',blank=True, null=True)
    foto_lado = models.ImageField(upload_to='alunos/foto_lado',blank=True, null=True)
    foto_verso = models.ImageField(upload_to='alunos/foto_verso',blank=True, null=True)
    avaliacao_fisica = models.ImageField(upload_to='alunos/avaliacao_fisica',blank=True, null=True) 
    exame_sangue = models.ImageField(upload_to='alunos/exame_sangue',blank=True, null=True)
    pago = models.BooleanField(default=False)
    plano = models.PositiveSmallIntegerField(choices=CHOICE, null=True, blank=True)
    mensalidade = models.DecimalField(max_digits=5, decimal_places=2,blank=True, null=True)
    vencimento_plano = models.DateField(blank=True, null=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
         
    
class Protocolo(models.Model):
    aluno = models.ForeignKey(Aluno, related_name='aluno_protocolo', on_delete=models.SET_NULL, null=True)
    coach = models.ForeignKey(Coach, related_name='coach_protocolo', on_delete=models.SET_NULL, null=True)
    protocolo = models.FileField(upload_to='protocolo', blank=True, null=True)
    carbo = models.IntegerField(blank=True, null=True)
    prot = models.IntegerField(blank=True, null=True)
    fat = models.IntegerField(blank=True, null=True)
    treino = models.CharField(max_length=155, blank=True, null=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    

class Feedback(models.Model):
    TOTALMENTE = 1
    REGULARMENTE =2
    NAO_SEGUI = 3
    
    CHOICE = (
        (TOTALMENTE, 'Totalmente'),
        (REGULARMENTE, 'Regularmente'),
        (NAO_SEGUI, 'Não Segui')
    )
    
    coach = models.ForeignKey(Coach, related_name='coach', on_delete=models.SET_NULL, null=True)
    aluno = models.ForeignKey(Aluno, related_name='aluno', on_delete=models.SET_NULL, null=True)
    protocolo = models.ForeignKey(Protocolo, related_name='protocolo_feedback', on_delete=models.SET_NULL, null=True)
    retorno = models.ForeignKey('Retorno', related_name='retorno_feedback', on_delete=models.SET_NULL, null=True)

    peso_atual = models.DecimalField(max_digits=6, decimal_places=3)
    
    dieta = models.PositiveSmallIntegerField(choices=CHOICE)
    dificuldade_dieta = models.TextField(blank=True, null=True)

    suplemento = models.PositiveSmallIntegerField(choices=CHOICE)
    dificuldade_suplemento = models.TextField(blank=True, null=True)
    
    treino = models.PositiveSmallIntegerField(choices=CHOICE)
    dificuldade_treino = models.TextField(blank=True, null=True)
    
    aerobico = models.PositiveSmallIntegerField(choices=CHOICE)
    dificuldade_aerobico = models.TextField(blank=True, null=True)
    
    melhorou = models.TextField(blank=True, null=True)
    pode_melhorar = models.TextField(blank=True, null=True)

    foto_frente = models.ImageField(upload_to='alunos/foto_frente', blank=True, null=True)
    foto_lado = models.ImageField(upload_to='alunos/foto_lado', blank=True, null=True)
    foto_verso = models.ImageField(upload_to='alunos/foto_verso', blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)
    
    comprometimento = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    avalia_coach = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)]
    )
    
    sugestoes = models.TextField(blank=True, null=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    atendido = models.BooleanField(default=False)
    
    def __str__(self):
        return self.aluno.email
    
   
class Retorno(models.Model):

    feedback = models.OneToOneField(Feedback, related_name='feedback', on_delete=models.SET_NULL, null=True)
    protocolo = models.ForeignKey(Protocolo, related_name='retorno_protocolo', on_delete=models.SET_NULL, null=True,blank=True)
    peso_comentario = models.CharField(max_length=255)
    dieta_comentario = models.TextField(blank=True, null=True)
    suplemento_comentario = models.TextField(blank=True, null=True)
    treino_comentario = models.TextField(blank=True, null=True) 
    aerobico_comentario = models.TextField(blank=True, null=True)
    melhorias_comentario = models.TextField(blank=True, null=True)
    fotos_comentario = models.TextField(max_length=255)
    video_comentario = models.TextField(max_length=255, blank=True, null=True) 
    sugestoes_comentario = models.TextField(blank=True, null=True)
    comentarios_finais = models.TextField(null=True, blank=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)


    
    
class Replica(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    retorno = models.ForeignKey(Retorno, related_name='retorno', on_delete=models.SET_NULL, null=True)
    dieta = models.TextField(null=True, blank=True)
    suplemento = models.TextField(null=True, blank=True)
    treino = models.TextField(null=True, blank=True) 
    aerobico = models.TextField(null=True, blank=True)
    demais_assuntos = models.TextField(null=True, blank=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    def __str__(self):
        return self.aluno.email