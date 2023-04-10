from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Replica, Retorno, Feedback, Protocolo, Aluno, Coach
from django.forms.widgets import DateInput
from django.core.validators import MinValueValidator, MaxValueValidator




class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        email = cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already exists, try another one...")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")


class UserUpdateForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email address must be unique')
        return email


class PerfilAluno(forms.ModelForm):

    class Meta:
        model = Aluno
        fields="__all__"
        exclude = ['idade', 'mensalidade','pago','user','plano','vencimento_plano','coach','atualizado_em','cadastrado_em','peso_atual',]                    
        # Add Bootstrap styling to form fields
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'sobrenome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'celular': forms.TextInput(attrs={'class': 'form-control'}),
            'altura': forms.NumberInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'enfermidades': forms.TextInput(attrs={'class': 'form-control'}),
            'medicamentos': forms.TextInput(attrs={'class': 'form-control'}),
            'lesao': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo_curto': forms.TextInput(attrs={'class': 'form-control'}),
            'objetivo_longo': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'avatar': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'foto_frente': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'foto_lado': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'foto_verso': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'avaliacao_fisica': forms.ClearableFileInput(attrs={'class':'form-control'}),
            'exame_sangue': forms.ClearableFileInput(attrs={'class':'form-control'}),

            # Add more form fields here as needed
        }    
        
class GerenciarAluno(forms.ModelForm):

    class Meta:
        model = Aluno
        fields=['coach', 'plano','mensalidade', 'vencimento_plano','pago',]
        
        # add a DateInput widget to data_nascimento field
    vencimento_plano = forms.DateField(widget=DateInput(attrs={'type': 'date'}))    

class PerfilCoach(forms.ModelForm):

    class Meta:
        model = Coach
        fields="__all__"
        exclude = ['user','atualizado_em','cadastrado_em',]
        
        # add a DateInput widget to data_nascimento field
    data_nascimento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))    
        
        
class NovoProtocolo(forms.ModelForm):

    class Meta:
        model = Protocolo
        fields="__all__"
        exclude = ['coach','aluno','atualizado_em','cadastrado_em','kcal',]
        widgets = {
            'protocolo' : forms.ClearableFileInput(attrs={'class':'form-control'}),
            'carbo' : forms.TextInput(attrs={'class':'form-control'} ),
            'prot' : forms.TextInput(attrs={'class':'form-control'} ),
            'fat' : forms.TextInput(attrs={'class':'form-control'} ),
            'treino' : forms.TextInput(attrs={'class':'form-control'}),
        }
        
        
class NovoFeedback(forms.ModelForm):

    class Meta:
        model = Feedback
        fields="__all__"
        exclude = ['retorno','coach','aluno','atualizado_em','cadastrado_em','atendido','protocolo',]
        widgets = {
            'foto_frente' : forms.ClearableFileInput(attrs={'class':'form-control'}),
            'foto_lado' : forms.ClearableFileInput(attrs={'class':'form-control'}),
            'foto_verso' : forms.ClearableFileInput(attrs={'class':'form-control'}),
            'video' : forms.TextInput(attrs={'class':'form-control'}),
            'peso_atual' : forms.NumberInput(attrs={'class':'form-control'} ),
            'dieta' : forms.Select(attrs={'class':'form-control'} ),
            'dificuldade_dieta' : forms.Textarea(attrs={'class':'form-control'} ),
            'treino' : forms.Select(attrs={'class':'form-control'}),
            'dificuldade_treino' : forms.Textarea(attrs={'class':'form-control'}),
            'suplemento' : forms.Select(attrs={'class':'form-control'} ),
            'dificuldade_suplemento' : forms.Textarea(attrs={'class':'form-control'} ),
            'aerobico' : forms.Select(attrs={'class':'form-control'} ),
            'dificuldade_aerobico' : forms.Textarea(attrs={'class':'form-control'} ),
            'melhorou' : forms.TextInput(attrs={'class':'form-control'} ),
            'pode_melhorar' : forms.TextInput(attrs={'class':'form-control'} ),
            'comprometimento' : forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'avalia_coach' : forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'sugestoes' : forms.Textarea(attrs={'class':'form-control'})
        }
        
class NovoRetorno(forms.ModelForm):

    class Meta:
        model = Retorno
        fields="__all__"
        exclude = ['atualizado_em','cadastrado_em','feedback','protocolo','aluno','coach','replica']
        
class NovaReplica(forms.ModelForm):

    class Meta:
        model = Replica
        fields="__all__"
        exclude = ['atualizado_em','cadastrado_em','author','retorno',]
        widgets = {
            'dieta' : forms.TextInput(attrs={'class':'form-control'} ),
            'treino' : forms.TextInput(attrs={'class':'form-control'}),
            'suplemento' : forms.TextInput(attrs={'class':'form-control'} ),
            'aerobico' : forms.TextInput(attrs={'class':'form-control'} ),
            'demais_assuntos' : forms.TextInput(attrs={'class':'form-control'} ),
            'pode_melhorar' : forms.TextInput(attrs={'class':'form-control'} ),
            'comprometimento' : forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'avalia_coach' : forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '10'}),
            'sugestoes' : forms.Textarea(attrs={'class':'form-control'})
        }