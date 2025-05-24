from django.db.models.signals import post_migrate ,post_save ,post_delete ,pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import Permission
from .custom_user import CustomUser
from .models import AppPermission ,Attachment
from django.conf import settings

@receiver(pre_delete, sender=Attachment)
def delete_attachment_file(sender, instance, **kwargs):

    if instance.file and instance.file.storage.exists(instance.file.name):
        instance.file.delete(save=False)



@receiver(post_save, sender=CustomUser)
def create_user_permission(sender, instance, created, **kwargs):
    if created:
        AppPermission.objects.create(user=instance, **settings.USER_DEFAULT_PERMISSIONS)
        
