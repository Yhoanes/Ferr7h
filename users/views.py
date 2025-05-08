from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import logout
from .forms import CustomLoginForm, AdminUpdateForm, UserForm, UserEditForm, RoleForm, PermissionForm
from .models import Role, SystemPermission
from django.urls import reverse
from .config import ACTION_CHOICES
import json

# Vista personalizada de Login
class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    authentication_form = CustomLoginForm

    def get_success_url(self):
        user = self.request.user
        profile = user.profile

        if user.is_superuser and not profile.perfil_actualizado:
            return reverse('admin_update')
        return reverse('dashboard')

@login_required
def admin_update(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = AdminUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            profile.perfil_actualizado = True
            profile.save()
            logout(request)
            return redirect(reverse('dashboard'))
    else:
        form = AdminUpdateForm(instance=user)
    
    return render(request, 'users/admin_update.html', {'form': form})

def signout(request):
    logout(request)
    return redirect('/users/login/')

@login_required
def users_list(request):
    query = request.GET.get('q')
    users = User.objects.all()

    if query:
        users = User.objects.filter(username__icontains=query)

    return render(request, 'users/users_list.html', {'users': users, 'query': query})

@login_required
def create_user(request):
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            role = Role.objects.get(id=request.POST.get("role"))
            profile = user.profile
            profile.role = role
            profile.save()

            return redirect('users_list')
    else:
        form = UserForm()

    return render(request, 'users/create_user.html', {'form': form, 'roles': roles})

@login_required
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile = user.profile
    roles = Role.objects.all()

    if request.method == 'POST':
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            role = Role.objects.get(id=request.POST.get("role"))
            profile.role = role
            profile.save()

            return redirect('users_list')
    else:
        form = UserEditForm(instance=user, initial={'role': profile.role})

    return render(request, 'users/edit_user.html', {'form': form, 'user': user, 'roles': roles})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if hasattr(user, "profile"):
        user.profile.delete()
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
            form.save_m2m()  # 🔥 Ahora `save_m2m()` funcionará correctamente

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
            role = form.save(commit=False)
            role.save()
            form.save_m2m()
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

            try:
                # 🔥 Convertimos JSON a texto separado por comas si es necesario
                selected_actions_list = json.loads(selected_actions) if isinstance(selected_actions, str) else selected_actions
                selected_actions_text = ",".join(selected_actions_list)
            except json.JSONDecodeError:
                selected_actions_text = ""

            new_permission.actions = selected_actions_text  # ✅ Guardamos como texto separado por comas
            new_permission.save()

            print(f"🔍 Permiso creado: {new_permission.name} - Acciones guardadas: {new_permission.actions}")  # 🔥 Debug

            return redirect("permissions_list")
        else:
            print("⚠️ Error en el formulario:", form.errors)

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
            selected_actions = request.POST.get("actions", "")

            # ✅ Si no hay acciones seleccionadas, aseguramos que no cause errores
            permission.actions = selected_actions if selected_actions else ""
            permission.save()

            return redirect("permissions_list")
        else:
            print("⚠️ Error en el formulario:", form.errors)

    else:
        form = PermissionForm(instance=permission)

    # ✅ Convertimos `actions` de texto a lista para mostrarlo correctamente en el formulario
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
