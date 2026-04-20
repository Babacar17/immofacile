import logging
from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify

logger = logging.getLogger('immofacile')


class Listing(models.Model):
    class Type(models.TextChoices):
        APARTMENT = 'apartment', 'Appartement'
        HOUSE     = 'house',     'Maison'
        ROOM      = 'room',      'Chambre'
        STUDIO    = 'studio',    'Studio'
        VILLA     = 'villa',     'Villa'
        OFFICE    = 'office',    'Bureau / Commerce'

    class Status(models.TextChoices):
        ACTIVE   = 'active',   'Disponible'
        RENTED   = 'rented',   'Loué'
        INACTIVE = 'inactive', 'Désactivé'

    owner        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='listings', db_index=True)
    title        = models.CharField(max_length=200)
    slug         = models.SlugField(max_length=220, unique=True, blank=True)
    description  = models.TextField()
    type         = models.CharField(max_length=20, choices=Type.choices, db_index=True)
    status       = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE, db_index=True)

    country      = models.CharField(max_length=60, default='Sénégal')
    city         = models.CharField(max_length=100, db_index=True)
    neighborhood = models.CharField(max_length=100, blank=True, db_index=True)
    address      = models.CharField(max_length=300, blank=True)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    price           = models.PositiveIntegerField(verbose_name='Loyer mensuel (FCFA)')
    price_charges   = models.PositiveIntegerField(default=0, verbose_name='Charges (FCFA)')
    deposit         = models.PositiveIntegerField(default=0, verbose_name='Caution (FCFA)')
    price_negotiable= models.BooleanField(default=False)

    surface       = models.PositiveIntegerField(null=True, blank=True)
    rooms         = models.PositiveSmallIntegerField(default=1)
    bedrooms      = models.PositiveSmallIntegerField(default=1)
    bathrooms     = models.PositiveSmallIntegerField(default=1)
    floor         = models.SmallIntegerField(null=True, blank=True)
    available_from= models.DateField(null=True, blank=True)

    furnished      = models.BooleanField(default=False)
    has_parking    = models.BooleanField(default=False)
    has_wifi       = models.BooleanField(default=False)
    has_ac         = models.BooleanField(default=False)
    has_garden     = models.BooleanField(default=False)
    has_pool       = models.BooleanField(default=False)
    has_security   = models.BooleanField(default=False)
    has_balcony    = models.BooleanField(default=False)
    has_elevator   = models.BooleanField(default=False)
    has_generator  = models.BooleanField(default=False)
    has_water_tank = models.BooleanField(default=False)
    pets_allowed   = models.BooleanField(default=False)

    is_featured  = models.BooleanField(default=False, db_index=True)
    views_count  = models.PositiveIntegerField(default=0, editable=False)
    created_at   = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at   = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(f'{self.title}-{self.city}')[:210]
            self.slug = base
            n = 1
            while Listing.objects.filter(slug=self.slug).exclude(pk=self.pk).exists():
                self.slug = f'{base}-{n}'; n += 1
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('listings:detail', kwargs={'pk': self.pk})

    def get_main_photo(self):
        return self.photos.filter(is_main=True).first() or self.photos.first()

    @property
    def has_coordinates(self):
        return bool(self.latitude and self.longitude)

    def __str__(self):
        return f'{self.title} — {self.city}'

    class Meta:
        verbose_name        = 'Annonce'
        verbose_name_plural = 'Annonces'
        ordering = ['-is_featured', '-created_at']
        indexes  = [
            models.Index(fields=['status', 'type']),
            models.Index(fields=['city', 'neighborhood']),
            models.Index(fields=['price']),
            models.Index(fields=['is_featured', 'status']),
        ]


class Photo(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='photos')
    image   = models.ImageField(upload_to='listings/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    is_main = models.BooleanField(default=False)
    order   = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ['order', 'id']

    def __str__(self):
        return f'Photo — {self.listing.title}'


class Favorite(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='favorites')
    listing  = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='favorited_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'listing')
        verbose_name    = 'Favori'

    def __str__(self):
        return f'{self.user} ❤ {self.listing.title}'
