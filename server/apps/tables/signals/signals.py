from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from apps.tables.models import Table


@receiver(post_save, sender=User)
def create_table(sender, instance, created, **kwargs):
    print('SIGNAL WAS CALLED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    if created:
        Table.objects.create(user=instance)
