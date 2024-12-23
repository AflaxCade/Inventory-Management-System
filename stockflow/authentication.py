from django.contrib.auth.models import User
from .models import Customer
from django.core.files.base import ContentFile
from urllib.parse import urlparse, unquote
import requests
import os

class EmailAuthBackend(object):
    """
    Authenticate using an e-mail address.
    """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
        except (User.DoesNotExist, User.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        try:    
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
        
def create_profile(backend, user, response, *args, **kwargs):
    """
    Create user profile for social authentication and save the social profile picture.
    """
    customer, created = Customer.objects.get_or_create(user=user)
    
    # Handle Google OAuth2
    if backend.name == 'google-oauth2':
        picture_url = response.get('picture')

    if picture_url:
        # Download the image
        r = requests.get(picture_url)
        if r.status_code == 200:
            # Parse the filename and add an appropriate extension
            parsed_url = urlparse(picture_url)
            filename = os.path.basename(unquote(parsed_url.path))
            filename, ext = os.path.splitext(filename)
            if ext.lower() not in ['.jpg', '.jpeg', '.png']:
                ext = '.jpg'  # Default to .jpg if no valid extension
            customer.profile_pic.save(f'{filename}{ext}', ContentFile(r.content), save=True)