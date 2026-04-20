import logging
from datetime import timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Count, Q, Sum
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View

from listings.models import Listing, Photo
from messaging.models import Message, VisitRequest
from agencies.models import AgencyReview

User = get_user_model()
logger = logging.getLogger('immofacile')

# ── Décorateur commun ─────────────────────────────────────────────────────────
def admin_required(view_func):
    return staff_member_required(view_func, login_url='/accounts/connexion/')


# ── VUE PRINCIPALE : tableau de bord ─────────────────────────────────────────
@admin_required
def dashboard_home(request):
    now   = timezone.now()
    today = now.date()
    week_ago  = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)

    # Stats globales
    stats = {
        'users_total':    User.objects.count(),
        'users_active':   User.objects.filter(is_active=True).count(),
        'users_week':     User.objects.filter(date_joined__gte=week_ago).count(),
        'tenants':        User.objects.filter(role='tenant').count(),
        'owners':         User.objects.filter(role='owner').count(),
        'agencies':       User.objects.filter(role='agency').count(),
        'agencies_pending': User.objects.filter(role='agency', is_verified=False, is_active=True).count(),

        'listings_total':  Listing.objects.count(),
        'listings_active': Listing.objects.filter(status='active').count(),
        'listings_rented': Listing.objects.filter(status='rented').count(),
        'listings_week':   Listing.objects.filter(created_at__gte=week_ago).count(),

        'messages_total':  Message.objects.count(),
        'messages_unread': Message.objects.filter(status='sent').count(),
        'visits_pending':  VisitRequest.objects.filter(status='pending').count(),
        'visits_total':    VisitRequest.objects.count(),
    }

    # Activité récente (7 derniers jours par jour)
    activity = []
    for i in range(6, -1, -1):
        day  = today - timedelta(days=i)
        day_end = day + timedelta(days=1)
        activity.append({
            'label':    day.strftime('%d/%m'),
            'users':    User.objects.filter(date_joined__date=day).count(),
            'listings': Listing.objects.filter(created_at__date=day).count(),
            'messages': Message.objects.filter(created_at__date=day).count(),
        })

    # Derniers utilisateurs inscrits
    recent_users = User.objects.order_by('-date_joined')[:8]

    # Dernières annonces
    recent_listings = Listing.objects.select_related('owner').order_by('-created_at')[:6]

    # Agences en attente de vérification
    pending_agencies = User.objects.filter(role='agency', is_verified=False, is_active=True).order_by('-date_joined')

    # Top villes
    top_cities = (Listing.objects.filter(status='active')
                  .values('city').annotate(n=Count('id')).order_by('-n')[:5])

    return render(request, 'dashboard/home.html', {
        'stats': stats,
        'activity': activity,
        'recent_users': recent_users,
        'recent_listings': recent_listings,
        'pending_agencies': pending_agencies,
        'top_cities': top_cities,
        'section': 'home',
    })


# ── UTILISATEURS ──────────────────────────────────────────────────────────────
@admin_required
def user_list(request):
    qs = User.objects.all().order_by('-date_joined')

    # Filtres
    role    = request.GET.get('role', '')
    status  = request.GET.get('status', '')
    q       = request.GET.get('q', '')
    verified= request.GET.get('verified', '')

    if role:     qs = qs.filter(role=role)
    if status == 'active':   qs = qs.filter(is_active=True)
    if status == 'inactive': qs = qs.filter(is_active=False)
    if verified == '1': qs = qs.filter(is_verified=True)
    if verified == '0': qs = qs.filter(is_verified=False)
    if q:
        qs = qs.filter(
            Q(username__icontains=q) | Q(email__icontains=q) |
            Q(first_name__icontains=q) | Q(last_name__icontains=q) |
            Q(agency_name__icontains=q)
        )

    return render(request, 'dashboard/users.html', {
        'users': qs, 'section': 'users',
        'filter_role': role, 'filter_status': status, 'filter_q': q, 'filter_verified': verified,
        'total': qs.count(),
    })


@admin_required
def user_detail(request, pk):
    u = get_object_or_404(User, pk=pk)
    listings = Listing.objects.filter(owner=u).order_by('-created_at')
    sent     = Message.objects.filter(sender=u).order_by('-created_at')[:10]
    received = Message.objects.filter(receiver=u).order_by('-created_at')[:10]
    visits   = VisitRequest.objects.filter(requester=u).order_by('-created_at')[:10]
    return render(request, 'dashboard/user_detail.html', {
        'u': u, 'listings': listings,
        'sent': sent, 'received': received, 'visits': visits,
        'section': 'users',
    })


@admin_required
def user_toggle_active(request, pk):
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, 'Vous ne pouvez pas désactiver votre propre compte.')
        return redirect('dashboard:user_detail', pk=pk)
    u.is_active = not u.is_active
    u.save(update_fields=['is_active'])
    action = 'activé' if u.is_active else 'désactivé'
    logger.warning('Admin %s a %s le compte de %s (id=%s)', request.user.username, action, u.username, u.pk)
    messages.success(request, f'Compte {u.display_name} {action}.')
    return redirect('dashboard:user_detail', pk=pk)


@admin_required
def user_verify(request, pk):
    u = get_object_or_404(User, pk=pk)
    u.is_verified = not u.is_verified
    u.verified_at = timezone.now() if u.is_verified else None
    u.save(update_fields=['is_verified', 'verified_at'])
    action = 'vérifié' if u.is_verified else 'dévérifié'
    logger.info('Admin %s a %s le compte de %s', request.user.username, action, u.username)
    messages.success(request, f'Compte {u.display_name} {action}.')
    return redirect('dashboard:user_detail', pk=pk)


@admin_required
def user_make_staff(request, pk):
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, 'Action non autorisée sur votre propre compte.')
        return redirect('dashboard:user_detail', pk=pk)
    u.is_staff = not u.is_staff
    u.save(update_fields=['is_staff'])
    action = 'promu admin' if u.is_staff else 'retiré des admins'
    logger.warning('Admin %s a %s %s', request.user.username, action, u.username)
    messages.success(request, f'{u.display_name} {action}.')
    return redirect('dashboard:user_detail', pk=pk)


@admin_required
def user_delete(request, pk):
    u = get_object_or_404(User, pk=pk)
    if u == request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('dashboard:user_detail', pk=pk)
    if request.method == 'POST':
        name = u.display_name
        logger.warning('Admin %s a SUPPRIMÉ le compte %s (id=%s)', request.user.username, u.username, u.pk)
        u.delete()
        messages.success(request, f'Compte {name} supprimé.')
        return redirect('dashboard:users')
    return render(request, 'dashboard/confirm.html', {
        'title':   f'Supprimer {u.display_name} ?',
        'message': f'Cette action supprimera définitivement le compte de {u.display_name} ainsi que toutes ses annonces et messages.',
        'danger':  True,
        'back_url': request.META.get('HTTP_REFERER', '/dashboard/utilisateurs/'),
        'section': 'users',
    })


# ── ANNONCES ─────────────────────────────────────────────────────────────────
@admin_required
def listing_list(request):
    qs = Listing.objects.select_related('owner').order_by('-created_at')

    status   = request.GET.get('status', '')
    type_    = request.GET.get('type', '')
    city     = request.GET.get('city', '')
    featured = request.GET.get('featured', '')
    q        = request.GET.get('q', '')

    if status:   qs = qs.filter(status=status)
    if type_:    qs = qs.filter(type=type_)
    if city:     qs = qs.filter(city__icontains=city)
    if featured == '1': qs = qs.filter(is_featured=True)
    if q:        qs = qs.filter(Q(title__icontains=q) | Q(owner__username__icontains=q))

    cities = Listing.objects.values_list('city', flat=True).distinct().order_by('city')

    return render(request, 'dashboard/listings.html', {
        'listings': qs, 'section': 'listings',
        'filter_status': status, 'filter_type': type_,
        'filter_city': city, 'filter_featured': featured, 'filter_q': q,
        'cities': cities, 'total': qs.count(),
    })


@admin_required
def listing_toggle_status(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    new_status = request.POST.get('status', 'active')
    if new_status in ('active', 'rented', 'inactive'):
        listing.status = new_status
        listing.save(update_fields=['status'])
        logger.info('Admin %s a changé le statut de l\'annonce %s → %s', request.user.username, pk, new_status)
        messages.success(request, f'Annonce "{listing.title}" → {listing.get_status_display()}')
    return redirect(request.META.get('HTTP_REFERER', '/dashboard/annonces/'))


@admin_required
def listing_toggle_featured(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    listing.is_featured = not listing.is_featured
    listing.save(update_fields=['is_featured'])
    action = 'mise en vedette' if listing.is_featured else 'retirée de la vedette'
    messages.success(request, f'Annonce "{listing.title}" {action}.')
    return redirect(request.META.get('HTTP_REFERER', '/dashboard/annonces/'))


@admin_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    if request.method == 'POST':
        title = listing.title
        logger.warning('Admin %s a supprimé l\'annonce %s (id=%s)', request.user.username, title, pk)
        listing.delete()
        messages.success(request, f'Annonce "{title}" supprimée.')
        return redirect('dashboard:listings')
    return render(request, 'dashboard/confirm.html', {
        'title':   f'Supprimer "{listing.title}" ?',
        'message': 'Cette annonce et toutes ses photos seront supprimées définitivement.',
        'danger':  True,
        'back_url': '/dashboard/annonces/',
        'section': 'listings',
    })


# ── MESSAGES & VISITES ────────────────────────────────────────────────────────
@admin_required
def messages_list(request):
    msgs   = Message.objects.select_related('sender','receiver','listing').order_by('-created_at')[:100]
    visits = VisitRequest.objects.select_related('requester','listing').order_by('-created_at')[:50]
    return render(request, 'dashboard/messages.html', {
        'msgs': msgs, 'visits': visits, 'section': 'messages',
    })


# ── AGENCES ───────────────────────────────────────────────────────────────────
@admin_required
def agencies_list(request):
    agencies = User.objects.filter(role='agency').annotate(
        listing_count=Count('listings', filter=Q(listings__status='active')),
        review_count=Count('reviews'),
    ).order_by('-date_joined')
    return render(request, 'dashboard/agencies.html', {
        'agencies': agencies, 'section': 'agencies',
    })


# ── STATS JSON (graphique) ────────────────────────────────────────────────────
@admin_required
def stats_json(request):
    today = timezone.now().date()
    data  = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        data.append({
            'date':     day.strftime('%d/%m'),
            'users':    User.objects.filter(date_joined__date=day).count(),
            'listings': Listing.objects.filter(created_at__date=day).count(),
            'messages': Message.objects.filter(created_at__date=day).count(),
        })
    return JsonResponse({'data': data})


# ── LOGS ─────────────────────────────────────────────────────────────────────
@admin_required
def logs_view(request):
    import os
    from django.conf import settings
    log_type = request.GET.get('type', 'app')
    log_files = {
        'app':      'app.log',
        'errors':   'errors.log',
        'requests': 'requests.log',
        'security': 'security.log',
    }
    filename = log_files.get(log_type, 'app.log')
    path     = settings.LOGS_DIR / filename
    lines    = []
    if path.exists():
        with open(path, encoding='utf-8', errors='replace') as f:
            lines = f.readlines()[-200:]   # 200 dernières lignes
        lines = [l.rstrip() for l in reversed(lines)]

    return render(request, 'dashboard/logs.html', {
        'lines': lines, 'log_type': log_type, 'filename': filename,
        'section': 'logs',
    })
