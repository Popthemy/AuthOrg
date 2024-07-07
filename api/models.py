
from django.db import models
from django.conf import settings
from uuid import uuid4
# Create your models here.
 
class Organisation(models.Model):
    id = models.CharField(max_length=36, primary_key=True, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='organisations')

    def __str__(self):
        return self.name

    
    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid4())
        super(Organisation, self).save(*args, **kwargs)