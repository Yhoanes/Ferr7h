from django.db import models
from django.contrib.auth.models import User
from .config import ACTION_CHOICES

# Modelo de Roles
class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.ManyToManyField("SystemPermission", blank=True)  # ✅ Relación ManyToMany

    def __str__(self):
        return self.name

# Perfil de Usuario
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    perfil_actualizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.role.name if self.role else 'Sin rol'}"

# Modelo de Permisos del Sistema
class SystemPermission(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    actions = models.TextField(default="")  

    module = models.CharField(
        max_length=50,
        choices=[("usuario", "Usuarios")],  # ✅ Solo el módulo 'usuario' por ahora
        default="usuario"
    )  # 🔥 Nuevo campo para identificar el módulo

    @staticmethod
    def get_available_actions():
        return ACTION_CHOICES

    def set_actions(self, actions_list):
        """Convierte una lista de acciones en un string separado por comas."""
        self.actions = ",".join(actions_list)

    def get_actions(self):
        """Convierte el string separado por comas en una lista de acciones."""
        return self.actions.split(",") if self.actions else []

    def __str__(self):
        return self.name
