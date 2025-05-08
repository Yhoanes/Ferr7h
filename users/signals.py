from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Role

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)

        if instance.is_superuser:
            admin_role, created = Role.objects.get_or_create(name="Administrador")
            profile.role = admin_role
            profile.save()