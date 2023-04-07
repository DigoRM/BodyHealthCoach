# Generated by Django 3.2.18 on 2023-04-07 23:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0009_auto_20230331_2052'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coach',
            old_name='foto_perfil',
            new_name='avatar',
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_fisica',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/avaliacao_fisica'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/avatar'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='exame_sangue',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/exame_sangue'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_frente',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_frente'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_lado',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_lado'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_verso',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_verso'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aluno', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_frente',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_frente'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_lado',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_lado'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_verso',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_verso'),
        ),
    ]