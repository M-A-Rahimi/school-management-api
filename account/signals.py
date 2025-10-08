from django.db.models.signals import pre_save, post_save
from django.db import transaction
from django.dispatch import receiver
from .models import QueueSignUp
from account.models import User
import string, secrets


def generate_random_password(length=12):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()"
    return ''.join(secrets.choice(alphabet) for _ in range(length))


@receiver(pre_save, sender=QueueSignUp)
def cache_old_status(sender, instance, **kwargs):
    """
        Caches the previous status of a QueueSignUp instance before saving.

        Purpose:
            - Stores the old 'status' in a temporary attribute (_old_status) on the instance.
            - This allows post_save signals to detect status changes.
        
        Functionality:
            - If instance already exists in the database:
                - Retrieve its current status and store in _old_status.
            - If instance is new:
                - _old_status is set to None.
    """
    if instance.pk:
        try:
            instance._old_status = sender.objects.get(pk=instance.pk).status
        except sender.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=QueueSignUp)
def create_user_when_accepted(sender, instance, created, **kwargs):
    """
    Automatically creates a User when a QueueSignUp is accepted.

    Purpose:
        - When the status of a QueueSignUp changes to 'accepted' ('a'), create a corresponding User account.
        - Ensures no duplicate user is created with the same national_code.
    
    Functionality:
        - Checks that the instance is not newly created (created=False).
        - Checks that previous status was not 'a' and current status is 'a'.
        - Generates a secure random password.
        - Creates a User using create_user() to hash the password.
        - Uses a database transaction to ensure atomicity.
        - TODO: Send an email to the user asynchronously (e.g., with Celery).
    """
    if not created and getattr(instance, '_old_status', None) != 'a' and instance.status == 'a':
        if not User.objects.filter(national_code=instance.national_code).exists():
            password = generate_random_password()
            print(password)
            with transaction.atomic():
                User.objects.create_user(
                    username=instance.national_code,
                    email=instance.email,
                    first_name=instance.first_name,
                    last_name=instance.last_name,
                    national_code=instance.national_code,
                    password=password
                )

