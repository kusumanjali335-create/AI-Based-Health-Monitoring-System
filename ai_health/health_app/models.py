from django.db import models
from django.contrib.auth.models import User


class HealthHistory(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=100)

    age = models.IntegerField()

    heart = models.CharField(max_length=30)

    diabetes = models.CharField(max_length=30)

    kidney = models.CharField(max_length=30)

    stroke = models.CharField(max_length=30)

    score = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name