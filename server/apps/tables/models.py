from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Table(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data_table = models.FileField(upload_to='data_tables', blank=True, null=True)
    last_modify = models.DateTimeField(auto_now=True)
    sizeof = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f'{self.user.username} TABLE'


@receiver(post_save, sender=User)
def create_table(sender, instance, created, **kwargs):
    if created:
        Table.objects.create(user=instance)
