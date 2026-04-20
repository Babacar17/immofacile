from django.db import models
from django.conf import settings

class AgencyReview(models.Model):
    agency   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='reviews', limit_choices_to={'role':'agency'})
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                  related_name='given_reviews')
    rating   = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    comment  = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together     = ('agency','reviewer')
        verbose_name        = 'Avis agence'
        verbose_name_plural = 'Avis agences'
        ordering            = ['-created_at']

    def __str__(self):
        return f'Avis de {self.reviewer} sur {self.agency} ({self.rating}/5)'
