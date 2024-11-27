from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Info(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news = models.CharField(max_length=1500, blank=True, null=True)
    result = models.BooleanField(default=0, blank=True, null=True)
    created_on = models.DateTimeField(auto_now=True)
