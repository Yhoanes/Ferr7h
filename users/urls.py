from django.urls import path
from .views import CustomLoginView, admin_update, signout, users_list, create_user, edit_user, delete_user, roles_list, create_role, edit_role, delete_role, permissions_list, create_permission, edit_permission, delete_permission

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('admin-update/', admin_update, name='admin_update'),
    path('logout/', signout, name='logout'),
    path('', users_list, name='users_list'),
    path('create/', create_user, name='create_user'),
    path('edit/<int:user_id>/', edit_user, name='edit_user'),
    path('delete/<int:user_id>/', delete_user, name='delete_user'),
    path('roles/', roles_list, name='roles_list'),
    path('roles/create/', create_role, name='create_role'),
    path('roles/edit/<int:role_id>/', edit_role, name='edit_role'),
    path('roles/delete/<int:role_id>/', delete_role, name='delete_role'),
    path('permissions/', permissions_list, name='permissions_list'),
    path('permissions/create/', create_permission, name='create_permission'),
    path('permissions/edit/<int:permission_id>/', edit_permission, name='edit_permission'),
    path('permissions/delete/<int:permission_id>/', delete_permission, name='delete_permission'),

]
