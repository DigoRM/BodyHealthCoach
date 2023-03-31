# Generated by Django 3.2.18 on 2023-03-31 20:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20230331_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='coach',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='aluno_coach', to='accounts.coach'),
        ),
    ]
