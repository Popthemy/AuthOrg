from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from uuid import uuid4

from .models import Organisation

@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_organisation_when_new_user(sender,created,instance,**kwargs):
  if created:
    user = instance
    organisation = Organisation.objects.create(
      id = str(uuid4()),
      name= f"{user.first_name}'s Organisation"
    )
    organisation.user.add(instance) # direct assignment to MANYTOMANY field not allowed we have to use the set(),add(),remove() to manage the rel