from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Coach, Aluno

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.is_staff:
            coach = Coach.objects.create(user=instance, nome=instance.username,email=instance.email)
            coach.save()
        else:
            aluno = Aluno.objects.create(user=instance, nome=instance.username,email=instance.email)
            aluno.save()
    else:
        if instance.is_staff:
            instance.coach.save()
        else:
            instance.aluno.save()
