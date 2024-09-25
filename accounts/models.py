from django.db import models
from django.core.validators import validate_integer
from django.contrib.auth.models import AbstractBaseUser 

from .managers import UserManager
from .validators import validate_phone , validate_len_phone
# Create your models here.



class User(AbstractBaseUser):
    username = models.CharField(max_length=50 , unique=True)
    name = models.CharField(max_length=255)
    lastname= models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name','lastname','email']

    objects = UserManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm(self , perm , obj=None):
        return True
    
    def has_module_perms(self , app_label):
        return True
    
    @property
    def is_staff(self):
        return self.is_admin
    