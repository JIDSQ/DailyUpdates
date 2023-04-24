from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
import uuid
from rest_framework_simplejwt.tokens import RefreshToken
# Create your models here.

class AccountManager(BaseUserManager):
    def create_user (self, email, password=None, **extra_fields):
     if not email:
         raise ValueError('User must have an email address') 
     email = self.normalize_email(email)
     user = self.model(email=email, **extra_fields)
     user.set_password(password)
     user.save(using = self._db)
     return user
    
    def create_superuser (self, email, password, **extra_fields):
     user = self.create_user (email, password, **extra_fields)
     user.is_staff = True
     user.is_superuser = True
     user.save (using=self._db)
     return user

class Account(AbstractUser):

    userID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.CharField(max_length=120, unique=True)
    role = models.CharField(max_length=20, default='admin', choices=(('admin', 'Admin'), ('staff', 'Staff')))
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    username = None
    REQUIRED_FIELDS = ['role']
    objects = AccountManager()

    @property
    def profile(self):
        return self.profile


class Profile(models.Model):
    user = models.OneToOneField(Account, primary_key= True, on_delete=models.CASCADE)
    firstName = models.CharField(max_length=100, null=False)
    lastName =  models.CharField(max_length=100, null=False)
    position =  models.CharField(max_length=100, null=False)

    
class DailyUpdate(models.Model):
    updateID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    owner = models.ForeignKey(Account, on_delete=models.CASCADE)
    accomplishedTask = models.TextField()
    inProgressTask = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    blocker = models.TextField()

class Announcement(models.Model):
    announcementID = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adminID= models.ForeignKey(Account, on_delete=models.CASCADE)
    title =  models.CharField(max_length=100, null=False)
    description = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    lastEdited = models.DateTimeField(auto_now=True)





