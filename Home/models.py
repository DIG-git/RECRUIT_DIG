from django.db import models
from authentication.models import User


class Big5result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    openness = models.FloatField(blank=True, null=True)
    conscientiousness = models.FloatField(blank=True, null=True)
    extraversion = models.FloatField(blank=True, null=True)
    agreeableness = models.FloatField(blank=True, null=True)
    neuroticism = models.FloatField(blank=True, null=True)

