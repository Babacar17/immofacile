import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm

logger = logging.getLogger('immofacile')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('listings:home')
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        logger.info('Nouvel utilisateur : %s role=%s', user.username, user.role)
        messages.success(request, f'Bienvenue {user.display_name} ! Votre compte a été créé.')
        return redirect('listings:home')
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('listings:home')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        logger.info('Connexion : %s', form.get_user().username)
        messages.success(request, 'Connexion réussie !')
        return redirect(request.GET.get('next', 'listings:home'))
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logger.info('Déconnexion : %s', request.user.username)
    logout(request)
    messages.info(request, 'Vous êtes déconnecté.')
    return redirect('listings:home')


@login_required
def profile_view(request):
    form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Profil mis à jour !')
        return redirect('accounts:profile')
    return render(request, 'accounts/profile.html', {'form': form})
