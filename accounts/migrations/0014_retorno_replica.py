# Generated by Django 3.2.18 on 2023-04-10 17:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20230410_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='retorno',
            name='replica',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='replica', to='accounts.protocolo'),
        ),
    ]