# Generated by Django 3.2.18 on 2023-04-28 00:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_auto_20230423_1645'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='aluno',
            name='peso_atual',
        ),
    ]