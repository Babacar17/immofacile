import logging
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

logger = logging.getLogger('immofacile')


class User(AbstractUser):
    class Role(models.TextChoices):
        TENANT = 'tenant', 'Locataire'
        OWNER  = 'owner',  'Propriétaire'
        AGENCY = 'agency', 'Agence immobilière'

    role        = models.CharField(max_length=10, choices=Role.choices, default=Role.TENANT, db_index=True)
    phone       = models.CharField(max_length=20, blank=True)
    whatsapp    = models.CharField(max_length=20, blank=True)
    avatar      = models.ImageField(upload_to='avatars/%Y/%m/', blank=True, null=True)
    bio         = models.TextField(blank=True, max_length=500)
    city        = models.CharField(max_length=100, blank=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(null=True, blank=True)
    notify_messages = models.BooleanField(default=True)
    notify_visits   = models.BooleanField(default=True)
    agency_name    = models.CharField(max_length=200, blank=True)
    agency_address = models.CharField(max_length=300, blank=True)
    agency_website = models.URLField(blank=True)
    agency_license = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def is_tenant(self): return self.role == self.Role.TENANT
    @property
    def is_owner(self):  return self.role == self.Role.OWNER
    @property
    def is_agency(self): return self.role == self.Role.AGENCY

    @property
    def display_name(self):
        if self.is_agency and self.agency_name:
            return self.agency_name
        full = self.get_full_name()
        return full.strip() if full.strip() else self.username

    @property
    def avg_rating(self):
        reviews = self.reviews.all()
        if not reviews.exists(): return 0
        return round(sum(r.rating for r in reviews) / reviews.count(), 1)

    def mark_verified(self):
        self.is_verified = True
        self.verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'verified_at'])
        logger.info('Compte vérifié : %s (id=%s)', self.username, self.pk)

    def __str__(self):
        return f'{self.display_name} ({self.get_role_display()})'

    class Meta:
        verbose_name        = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        indexes = [
            models.Index(fields=['role', 'is_verified']),
        ]
