from django.contrib import admin
from .models import Aluno, Coach, Feedback, Retorno

# Register your models here.
admin.site.register(Aluno)
admin.site.register(Coach)

admin.site.register(Feedback)
admin.site.register(Retorno)