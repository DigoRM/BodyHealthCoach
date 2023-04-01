# Generated by Django 3.2.18 on 2023-03-28 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_aluno_peso_atual'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='foto_frente',
            new_name='foto_perfil',
        ),
        migrations.AddField(
            model_name='aluno',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/avatar'),
        ),
    ]