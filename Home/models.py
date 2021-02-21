from django.db import models
from django.urls import reverse

from authentication.models import User


class Big5result(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    openness = models.FloatField(blank=True, null=True)
    conscientiousness = models.FloatField(blank=True, null=True)
    extraversion = models.FloatField(blank=True, null=True)
    agreeableness = models.FloatField(blank=True, null=True)
    neuroticism = models.FloatField(blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=40, blank=True, null=True)
    slug = models.SlugField(max_length=4, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_path(self):
        return reverse('job_category', kwargs={'id': self.slug})

    def get_absolute_url(self):
        return reverse('job_list')
