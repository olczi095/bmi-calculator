from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import CalculatedData, Person


@receiver(post_save, sender=User)
def update_person_name(sender, instance, created, **kwargs):
    if created:
        return
    try:
        person = Person.objects.get(user=instance)
    except Person.DoesNotExist:
        return

    if instance.first_name and instance.last_name:
        person.name = f"{instance.first_name} {instance.last_name}"
    else:
        person.name = instance.username
    person.save()


@receiver(post_save, sender=Person)
def update_or_create_calculated_data(sender, instance, created, **kwargs):
    if created:
        CalculatedData.objects.create(person=instance, pal=instance.pal)
    else:
        instance.calculated_data.pal = instance.pal
        instance.calculated_data.save()
