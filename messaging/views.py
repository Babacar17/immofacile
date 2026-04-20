import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Message, VisitRequest
from .forms import MessageForm, VisitRequestForm
from listings.models import Listing

logger = logging.getLogger('immofacile')


@login_required
def inbox(request):
    received = Message.objects.filter(receiver=request.user).select_related('sender','listing')
    sent     = Message.objects.filter(sender=request.user).select_related('receiver','listing')
    for msg in received.filter(status='sent'):
        msg.mark_read()
    return render(request, 'messaging/inbox.html', {'received': received, 'sent': sent})


@login_required
def send_message(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    if listing.owner == request.user:
        messages.warning(request, 'Vous ne pouvez pas vous envoyer un message.')
        return redirect('listings:detail', pk=listing_pk)
    form = MessageForm(request.POST or None)
    if form.is_valid():
        msg = form.save(commit=False)
        msg.sender   = request.user
        msg.receiver = listing.owner
        msg.listing  = listing
        msg.save()
        logger.info('Message envoyé : from=%s to=%s listing=%s', request.user.pk, listing.owner.pk, listing.pk)
        messages.success(request, 'Message envoyé avec succès !')
        return redirect('listings:detail', pk=listing_pk)
    return render(request, 'messaging/send.html', {'form': form, 'listing': listing})


@login_required
def request_visit(request, listing_pk):
    listing = get_object_or_404(Listing, pk=listing_pk)
    form    = VisitRequestForm(request.POST or None)
    if form.is_valid():
        visit = form.save(commit=False)
        visit.listing   = listing
        visit.requester = request.user
        visit.save()
        logger.info('Demande visite : user=%s listing=%s date=%s', request.user.pk, listing.pk, visit.date)
        messages.success(request, 'Demande de visite envoyée !')
        return redirect('listings:detail', pk=listing_pk)
    return render(request, 'messaging/visit_request.html', {'form': form, 'listing': listing})


@login_required
def my_visits(request):
    visits = VisitRequest.objects.filter(requester=request.user).select_related('listing')
    return render(request, 'messaging/my_visits.html', {'visits': visits})


@login_required
def manage_visits(request):
    visits = VisitRequest.objects.filter(listing__owner=request.user).select_related('requester','listing')
    return render(request, 'messaging/manage_visits.html', {'visits': visits})


@login_required
def update_visit_status(request, visit_pk, status):
    visit = get_object_or_404(VisitRequest, pk=visit_pk, listing__owner=request.user)
    if status in ('accepted','declined','done','cancelled'):
        visit.status = status
        visit.save(update_fields=['status','updated_at'])
        messages.success(request, f'Visite : {visit.get_status_display()}')
    return redirect('messaging:manage_visits')
