# Generated by Django 3.2.18 on 2023-03-30 12:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_auto_20230328_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='aluno',
            name='mensalidade',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AddField(
            model_name='feedback',
            name='retorno',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='retorno_feedback', to='accounts.retorno'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='plano',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'BASIC'), (2, 'SILVER'), (3, 'GOLD'), (4, 'ATLETA')], null=True),
        ),
    ]