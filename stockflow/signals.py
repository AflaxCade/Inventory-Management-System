from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User, Group
from .models import Customer


@receiver(post_save, sender=User)
def customer_profile(sender, instance, created, **kwargs):
    """
    Signal to create a Customer profile when a new User is created.
    """
    if created:
        try:
            group, _ = Group.objects.get_or_create(name='customer')
            instance.groups.add(group)
            Customer.objects.create(
                user=instance,
                name=instance.username,
                email=instance.email
            )
            print(f'Customer profile created for user: {instance.username}')
        except Group.DoesNotExist:
            print('Group "customer" does not exist.')
        except Exception as e:
            print(f'Error creating customer profile: {e}')

@receiver(post_save, sender=Customer)
def update_user_email(sender, instance, **kwargs):
    """
    Signal to update the User email when the Customer email is updated.
    """
    user = instance.user
    if user:
        user.email = instance.email
        user.save()
        print(f'User email updated for user: {user.username}') 