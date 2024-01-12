from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

class User(AbstractUser, PermissionsMixin):

    username = models.CharField(max_length=765, null=False, unique=True)
    email = models.EmailField(null=False, unique=True)
    failed_logins = models.IntegerField(null=False, default=0)
    is_blocked = models.BooleanField(default=False)
    number_phone = models.CharField(max_length=1024, null=True, blank=True)
    internal_user=models.BooleanField(default=False)
    
    def __str__(self):
        return self.username