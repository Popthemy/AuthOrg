from django.db import models
from django.conf import settings

# Create your models here.


class Organisation(models.Model):
    org_id = models.CharField(max_length=36,primary_key=True,unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True,null=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='organisations')