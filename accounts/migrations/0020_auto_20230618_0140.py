# Generated by Django 3.2.18 on 2023-06-18 04:40

import accounts.storage_backends
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0019_auto_20230617_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='avaliacao_fisica',
            field=models.FileField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/avaliacao_fisica'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='avatar',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/avatar'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='exame_sangue',
            field=models.FileField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/exame_sangue'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_frente',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_frente'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_lado',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_lado'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='foto_verso',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_verso'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='avatar',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='coach/foto_perfil'),
        ),
        migrations.AlterField(
            model_name='coach',
            name='foto_certificado',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='coach/certificado'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='avaliacao_fisica',
            field=models.FileField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/avaliacao_fisica'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='exame_sangue',
            field=models.FileField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/exame_sangue'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_frente',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_frente'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_lado',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_lado'),
        ),
        migrations.AlterField(
            model_name='feedback',
            name='foto_verso',
            field=models.ImageField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='alunos/foto_verso'),
        ),
        migrations.AlterField(
            model_name='protocolo',
            name='protocolo',
            field=models.FileField(blank=True, max_length=333, null=True, storage=accounts.storage_backends.MediaStorage, upload_to='protocolo'),
        ),
    ]