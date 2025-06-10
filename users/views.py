from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import CustomLoginForm, AdminUpdateForm, UserForm, UserEditForm, RoleForm, PermissionForm
from .models import Role, SystemPermission, Profile  
from django.urls import reverse
from .config import ACTION_CHOICES
import json

# 🔥 Vista personalizada de Login
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        """ Redirigir según el estado del perfil del usuario """
        user = self.request.user
        profile = user.profile

        # ✅ Si el usuario es superadministrador y no ha actualizado su perfil, redirigir a actualización
        if user.is_superuser and not profile.perfil_actualizado:
            return reverse('admin_update')
        return reverse('dashboard')

# 🔥 Vista para actualizar perfil de administrador
@login_required
def admin_update(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = AdminUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.perfil_actualizado = True  # ✅ Se marca como actualizado
            profile.save()
            logout(request)
            return redirect(reverse('dashboard'))
    else:
        form = AdminUpdateForm(instance=user)
    
    return render(request, 'users/admin_update.html', {'form': form})

# 🔥 Cerrar sesión
def signout(request):
    logout(request)
    return redirect('/users/login/')

# 🔥 Lista de usuarios con búsqueda
@login_required
def users_list(request):
    query = request.GET.get('q')  # ✅ Capturamos parámetro de búsqueda
    users = User.objects.filter(username__icontains=query) if query else User.objects.all()  # ✅ Optimización

    return render(request, 'users/users_list.html', {'users': users, 'query': query})

# 🔥 Crear usuario con asignación de rol
@login_required
def create_user(request):
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # ✅ Evitar duplicados en perfiles
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = Role.objects.get(id=request.POST.get("role"))
            profile.save()

            return redirect('users_list')
    else:
        form = UserForm()

    return render(request, 'users/create_user.html', {'form': form, 'roles': roles})

# 🔥 Editar usuario y asignar nuevo rol
@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user.save()
            profile.role = Role.objects.get(id=request.POST.get("role"))
            profile.save()
            return redirect('users_list')
    else:
        form = UserEditForm(instance=user, initial={'role': profile.role})

    return render(request, 'users/edit_user.html', {'form': form, 'user': user, 'roles': roles})

# 🔥 Eliminar usuario con seguridad
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # ✅ Manejo seguro para evitar errores si no tiene perfil
    if hasattr(user, "profile"):
        getattr(user, "profile", None).delete()
    
    user.delete()
    return redirect("users_list")

# 🔥 Gestión de Roles
@login_required
def roles_list(request):
    roles = Role.objects.all()
    return render(request, 'roles/roles_list.html', {'roles': roles})

@login_required
def create_role(request):
    if request.method == "POST":
        form = RoleForm(request.POST)
        if form.is_valid():
            role = form.save(commit=False)  # ✅ Primero `commit=False`
            role.save()
            form.save_m2m()  # 🔥 Se guardan relaciones many-to-many correctamente

            return redirect("roles_list")
    else:
        form = RoleForm()

    return render(request, "roles/create_role.html", {"form": form})

@login_required
def edit_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    
    if request.method == "POST":
        form = RoleForm(request.POST, instance=role)
        if form.is_valid():
            form.save()  # ✅ Solo `form.save()`, ya que no hay `ManyToManyField`
            return redirect("roles_list")
    else:
        form = RoleForm(instance=role)
    
    return render(request, "roles/edit_role.html", {"form": form, "role": role})

@login_required
def delete_role(request, role_id):
    role = get_object_or_404(Role, id=role_id)
    role.delete()
    return redirect("roles_list")

# 🔥 Gestión de Permisos
@login_required
def permissions_list(request):
    permissions = SystemPermission.objects.all()
    return render(request, "permissions/permissions_list.html", {"permissions": permissions})

@login_required
def create_permission(request):
    available_actions = SystemPermission.get_available_actions()

    if request.method == "POST":
        form = PermissionForm(request.POST)
        if form.is_valid():
            new_permission = form.save(commit=False)
            selected_actions = request.POST.get("actions", "[]")

            # ✅ Manejo seguro de JSON para evitar errores
            try:
                selected_actions_list = json.loads(selected_actions) if isinstance(selected_actions, str) else selected_actions
                selected_actions_text = ",".join(selected_actions_list)
            except json.JSONDecodeError:
                selected_actions_text = ""

            new_permission.actions = selected_actions_text
            new_permission.save()

            return redirect("permissions_list")

    else:
        form = PermissionForm()

    return render(request, "permissions/create_permission.html", {
        "form": form,
        "available_actions": available_actions,
    })

@login_required
def edit_permission(request, permission_id):
    permission = get_object_or_404(SystemPermission, id=permission_id)

    if request.method == "POST":
        form = PermissionForm(request.POST, instance=permission)
        if form.is_valid():
            permission.actions = request.POST.get("actions", "") or ""  # ✅ Evitar valores `None`
            permission.save()
            return redirect("permissions_list")
    else:
        form = PermissionForm(instance=permission)

    selected_actions = permission.get_actions()
    available_actions = SystemPermission.get_available_actions()

    return render(request, "permissions/edit_permission.html", {
        "form": form,
        "permission": permission,
        "selected_actions": selected_actions,
        "available_actions": available_actions,
    })

@login_required
def delete_permission(request, permission_id):
    permission = get_object_or_404(SystemPermission, id=permission_id)
    permission.delete()
    return redirect("permissions_list")