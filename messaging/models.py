import logging
from django.db import models
from django.conf import settings
from listings.models import Listing

logger = logging.getLogger('immofacile')


class Message(models.Model):
    class Status(models.TextChoices):
        SENT     = 'sent',     'Envoyé'
        READ     = 'read',     'Lu'
        REPLIED  = 'replied',  'Répondu'
        ARCHIVED = 'archived', 'Archivé'

    sender   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    listing  = models.ForeignKey(Listing, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    body     = models.TextField()
    status   = models.CharField(max_length=10, choices=Status.choices, default=Status.SENT, db_index=True)
    read_at  = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes  = [models.Index(fields=['receiver','status'])]

    def mark_read(self):
        from django.utils import timezone
        if self.status == self.Status.SENT:
            self.status  = self.Status.READ
            self.read_at = timezone.now()
            self.save(update_fields=['status','read_at'])

    def __str__(self):
        return f'Message #{self.pk} {self.sender} → {self.receiver}'


class VisitRequest(models.Model):
    class Status(models.TextChoices):
        PENDING   = 'pending',   'En attente'
        ACCEPTED  = 'accepted',  'Acceptée'
        DECLINED  = 'declined',  'Refusée'
        CANCELLED = 'cancelled', 'Annulée'
        DONE      = 'done',      'Effectuée'

    listing    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='visit_requests')
    requester  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visit_requests')
    date       = models.DateField()
    time_slot  = models.TimeField()
    note       = models.TextField(blank=True, max_length=500)
    status     = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    owner_note = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Visite {self.listing.title} — {self.requester} le {self.date}'
