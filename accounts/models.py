from django.db import models
from django.contrib.auth.models import User


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
    foto_frente = models.ImageField(upload_to='coach/foto_perfil',blank=True, null=True)
    foto_certificado = models.ImageField(upload_to='coach/certificado',blank=True, null=True)


    def __str__(self):
        return self.email



class Aluno(models.Model):
    user = models.OneToOneField(User, related_name='aluno', on_delete=models.CASCADE)
    coach = models.OneToOneField(Coach, related_name='aluno_coach', on_delete=models.CASCADE, blank=True,null=True)
    nome = models.CharField(max_length=255,blank=True, null=True)
    sobrenome = models.CharField(max_length=255,blank=True, null=True)
    idade = models.IntegerField(blank=True, null=True)
    email = models.EmailField(max_length=255)
    celular = models.CharField(max_length=33,blank=True,null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    altura = models.DecimalField(max_digits=2, decimal_places=2,blank=True, null=True)
    peso = models.DecimalField(max_digits=3, decimal_places=2,blank=True, null=True)
    enfermidades = models.CharField(max_length=255,blank=True, null=True)
    medicamentos = models.CharField(max_length=255,blank=True, null=True)
    lesao = models.CharField(max_length=255,blank=True, null=True)
    objetivo_curto = models.CharField(max_length=255)
    objetivo_longo = models.CharField(max_length=255)
    foto_frente = models.ImageField(upload_to='alunos/foto_frente',blank=True, null=True)
    foto_lado = models.ImageField(upload_to='alunos/foto_lado',blank=True, null=True)
    foto_verso = models.ImageField(upload_to='alunos/foto_verso',blank=True, null=True)
    avaliacao_fisica = models.ImageField(upload_to='alunos/avaliacao_fisica',blank=True, null=True) 
    exame_sangue = models.ImageField(upload_to='alunos/exame_sangue',blank=True, null=True)
    pago = models.BooleanField(default=False)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
    
    


class Feedback(models.Model):
    TOTALMENTE = 1
    REGULARMENTE =2
    NAO_SEGUI = 3
    
    CHOICE = (
        (TOTALMENTE, 'Totalmente'),
        (REGULARMENTE, 'Regularmente'),
        (NAO_SEGUI, 'Não Segui')
    )
    
    
    aluno = models.OneToOneField(Aluno, related_name='aluno', on_delete=models.SET_NULL, null=True)
    peso_atual = models.DecimalField(max_digits=3, decimal_places=2)
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

    foto_frente = models.ImageField(upload_to='alunos/foto_frente')
    foto_lado = models.ImageField(upload_to='alunos/foto_lado')
    foto_verso = models.ImageField(upload_to='alunos/foto_verso')
    video = models.CharField(max_length=255)
    
    comprometimento = models.IntegerField(choices=(
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ))
    avalia_coach = models.IntegerField(choices=(
        (0, '0'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    ))
    
    sugestoes = models.TextField(blank=True, null=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
class Retorno(models.Model):

    feedback = models.OneToOneField(Feedback, related_name='feedback', on_delete=models.SET_NULL, null=True)
    protocolo = models.FileField(upload_to='protocolos', blank=True, null=True)
    peso_comentario = models.CharField(max_length=255)
    dieta_comentario = models.TextField(blank=True, null=True)
    dificuldade_dieta = models.TextField()
    suplemento_comentario = models.TextField()
    treino_comentario = models.TextField() 
    aerobico_comentario = models.TextField()
    melhorias_comentario = models.TextField()
    fotos_comentario = models.TextField(max_length=255)
    video = models.TextField(max_length=255, blank=True, null=True) 
    objetivos_comentario = models.TextField(max_length=255, blank=True, null=True)
    sugestoes_comentario = models.TextField(blank=True, null=True)
    comentarios_finais = models.TextField(null=True, blank=True)
    cadastrado_em = models.DateTimeField(auto_now=True)
    atualizado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    
    
class Protocolo(models.Model):
    aluno = models.OneToOneField(Aluno, related_name='aluno_protocolo', on_delete=models.SET_NULL, null=True)
    protocolo = models.FileField(upload_to='protocolos', blank=True, null=True)