from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect  # <-- agrega esto
from assets import jwt_views

urlpatterns = [
    # Home: redirige a la lista de assets
    path('', lambda request: redirect('assets:list'), name='home'),

    path('admin/', admin.site.urls),

    # Autenticación por sesiones (UI)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # CRUD de Assets
    path('assets/', include('assets.urls')),

    # Endpoints JWT
    path('auth/jwt/', jwt_views.jwt_issue, name='jwt_issue'),
    path('jwt-protected/', jwt_views.jwt_protected, name='jwt_protected'),
]