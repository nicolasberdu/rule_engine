from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.timezone import now

class User(AbstractUser, PermissionsMixin):

    username = models.CharField(max_length=765, null=False, unique=True)
    password = models.CharField(max_length=128, verbose_name='password', null=True, default=None, blank=True)
    email = models.EmailField(null=False, unique=True)
    failed_logins = models.IntegerField(null=False, default=0)
    is_blocked = models.BooleanField(default=False)
    number_phone = models.CharField(max_length=1024, null=True, blank=True)
    internal_user=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username
    
class Rule(models.Model):
    attribute = models.CharField(max_length=40, unique=True, blank=False)
    description = models.CharField(max_length=100, unique=True, blank=False)
    value = models.CharField(max_length=40, null=True, default=None)
    update_at = models.DateTimeField(default=now)

    

class ActivationLink(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    key = models.CharField(primary_key=True, max_length=40, unique=True)
    created_at = models.DateTimeField(default=now)

    @classmethod
    def generate_new_link(cls, user):
        key = get_random_string(length=40)
        activation_link = cls.objects.create(user=user, key=key)

        return activation_link
    
    def __str__(self):
        return self.key