from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Replica, Retorno, Feedback, Protocolo, Aluno, Coach
from django.forms.widgets import DateInput



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
        exclude = ['pago','user','plano','vencimento_plano','coach','atualizado_em','cadastrado_em',]    
        
        # add a DateInput widget to data_nascimento field
    data_nascimento = forms.DateField(widget=DateInput(attrs={'type': 'date'}))    
        
class GerenciarAluno(forms.ModelForm):

    class Meta:
        model = Aluno
        fields=['coach', 'plano', 'vencimento_plano','pago',]
        
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
        exclude = ['coach','aluno','atualizado_em','cadastrado_em',]
        
        
        
class NovoFeedback(forms.ModelForm):

    class Meta:
        model = Feedback
        fields="__all__"
        exclude = ['coach','aluno','atualizado_em','cadastrado_em','atendido','protocolo',]
        
        
class NovoRetorno(forms.ModelForm):

    class Meta:
        model = Retorno
        fields="__all__"
        exclude = ['atualizado_em','cadastrado_em','feedback','protocolo']
        
class NovaReplica(forms.ModelForm):

    class Meta:
        model = Replica
        fields="__all__"
        exclude = ['atualizado_em','cadastrado_em',]