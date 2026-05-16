from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    A model extending the default Django User model to include a profile picture.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} Profile'
