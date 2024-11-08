# Generated by Django 3.2.18 on 2023-03-31 23:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0008_alter_aluno_coach'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_fisica',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/avaliacao_fisica/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/avatar/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='exame_sangue',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/exame_sangue/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_frente',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_frente/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_lado',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_lado/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_verso',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_verso/'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aluno', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_frente',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_frente/'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_lado',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_lado/'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_verso',
            field=models.ImageField(blank=True, null=True, upload_to='alunos/foto_verso/'),
        ),
    ]
