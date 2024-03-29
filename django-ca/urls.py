import django.contrib.auth.views as auth_views

from sshkbase.forms import UserPasswordResetForm

"""django-ca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('sshkbase.urls')),

    path('admin/', admin.site.urls),
    path('password-reset', auth_views.PasswordResetView.as_view(
        template_name='registration/password-reset.html',
        form_class=UserPasswordResetForm), name='password_reset'),
    path('password-reset/sent', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password-reset-sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password-reset-confirm.html'), name='password_reset_confirm'),
    path('reset/complete', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password-reset-complete.html'), name='password_reset_complete'),

]
