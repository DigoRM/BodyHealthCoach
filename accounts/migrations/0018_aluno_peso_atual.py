# Generated by Django 3.2.18 on 2023-04-28 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_remove_aluno_peso_atual'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='peso_atual',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=4, null=True),
        ),
    ]