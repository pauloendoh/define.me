from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    q = models.TextField(null=False)
    a = models.TextField(null=True, blank=True)
    tag = models.CharField(max_length=20, null=True, blank=True)
    #priority = models.FloatField(validators=[MinValueValidator(1), MaxValueValidator(3)], null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['updated_at', 'tag']

