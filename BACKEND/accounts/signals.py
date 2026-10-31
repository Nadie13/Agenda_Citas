from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

@receiver(post_save,sender=Profile)
def add_user_to_clients_group(sender,instance,created,**kwargs):
    if created:
        clients,_=Group.objects.get_or_create(name='clientes')
        Group.objects.get_or_create(name='gestor')
        Group.objects.get_or_create(name='administrador')

        instance.user.groups.add(clients)