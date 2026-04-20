import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from .models import Listing, Favorite
from .forms import ListingForm, ListingSearchForm

logger = logging.getLogger('immofacile')


def _filter_listings(qs, form):
    if form.is_valid():
        q     = form.cleaned_data.get('q')
        type_ = form.cleaned_data.get('type')
        city  = form.cleaned_data.get('city')
        pmax  = form.cleaned_data.get('price_max')
        if q:     qs = qs.filter(Q(title__icontains=q)|Q(description__icontains=q)|Q(neighborhood__icontains=q))
        if type_: qs = qs.filter(type=type_)
        if city:  qs = qs.filter(city__icontains=city)
        if pmax:  qs = qs.filter(price__lte=pmax)
    return qs


def home(request):
    form     = ListingSearchForm(request.GET or None)
    listings = _filter_listings(Listing.objects.filter(status='active').select_related('owner'), form)
    featured = listings.filter(is_featured=True)[:3]
    recent   = listings.order_by('-created_at')[:9]
    return render(request, 'listings/home.html', {'form': form, 'featured': featured, 'recent': recent})


def listing_map(request):
    form     = ListingSearchForm(request.GET or None)
    listings = _filter_listings(Listing.objects.filter(status='active').select_related('owner'), form)
    mapped   = listings.exclude(latitude=None, longitude=None)
    unmapped = listings.filter(latitude=None, longitude=None)
    return render(request, 'listings/map.html', {
        'form': form, 'mapped': mapped, 'unmapped': unmapped, 'all_listings': listings,
    })


def listings_geojson(request):
    qs = Listing.objects.filter(status='active').exclude(latitude=None, longitude=None).select_related('owner')
    features = []
    for l in qs:
        photo = l.get_main_photo()
        features.append({
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [float(l.longitude), float(l.latitude)]},
            'properties': {
                'id': l.pk, 'title': l.title, 'price': l.price,
                'type': l.get_type_display(), 'type_key': l.type,
                'city': l.city, 'neighborhood': l.neighborhood,
                'rooms': l.rooms, 'surface': l.surface,
                'furnished': l.furnished, 'url': l.get_absolute_url(),
                'photo': photo.image.url if photo else None,
                'owner': l.owner.display_name, 'is_agency': l.owner.is_agency,
                'is_featured': l.is_featured,
            }
        })
    return JsonResponse({'type': 'FeatureCollection', 'features': features})


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    Listing.objects.filter(pk=pk).update(views_count=listing.views_count + 1)
    logger.debug('Vue annonce id=%s title=%s', pk, listing.title)
    is_favorite = (request.user.is_authenticated and
                   Favorite.objects.filter(user=request.user, listing=listing).exists())
    similar = Listing.objects.filter(type=listing.type, city=listing.city, status='active').exclude(pk=pk)[:3]
    return render(request, 'listings/detail.html', {
        'listing': listing, 'is_favorite': is_favorite, 'similar': similar,
    })


@login_required
def listing_create(request):
    if request.user.is_tenant:
        messages.error(request, 'Seuls les propriétaires et agences peuvent publier des annonces.')
        return redirect('listings:home')
    form = ListingForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        listing = form.save(commit=False)
        listing.owner = request.user
        listing.save()
        logger.info('Annonce créée : id=%s owner=%s', listing.pk, request.user.username)
        messages.success(request, 'Annonce publiée avec succès !')
        return redirect('listings:detail', pk=listing.pk)
    return render(request, 'listings/form.html', {'form': form, 'action': 'Publier'})


@login_required
def listing_edit(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    form = ListingForm(request.POST or None, request.FILES or None, instance=listing)
    if form.is_valid():
        form.save()
        messages.success(request, 'Annonce mise à jour.')
        return redirect('listings:detail', pk=listing.pk)
    return render(request, 'listings/form.html', {'form': form, 'action': 'Modifier'})


@login_required
def listing_delete(request, pk):
    listing = get_object_or_404(Listing, pk=pk, owner=request.user)
    if request.method == 'POST':
        logger.info('Annonce supprimée : id=%s owner=%s', listing.pk, request.user.username)
        listing.delete()
        messages.success(request, 'Annonce supprimée.')
        return redirect('listings:my_listings')
    return render(request, 'listings/confirm_delete.html', {'listing': listing})


@login_required
def my_listings(request):
    listings = Listing.objects.filter(owner=request.user)
    return render(request, 'listings/my_listings.html', {'listings': listings})


@login_required
def toggle_favorite(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, listing=listing)
    if not created:
        fav.delete()
        messages.info(request, 'Retiré des favoris.')
    else:
        messages.success(request, 'Ajouté aux favoris !')
    return redirect('listings:detail', pk=pk)


@login_required
def favorites(request):
    favs = Favorite.objects.filter(user=request.user).select_related('listing')
    return render(request, 'listings/favorites.html', {'favorites': favs})


# ── Health check pour Render ──────────────────────────────────────────────────
from django.http import HttpResponse

def health_check(request):
    """Endpoint de santé pour Render — retourne 200 OK"""
    return HttpResponse("OK", status=200)
