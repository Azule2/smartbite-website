from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    forget_password_token = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    images = models.ImageField(upload_to="static/images/", null=True,blank=True, height_field=None, width_field=None, max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']
    def __str__(self):
        return self.title