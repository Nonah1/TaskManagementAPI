from django.conf import settings
from django.db import models
from datetime import timedelta
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.
class Task(models.Model):
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [(PRIORITY_LOW,'Low'), (PRIORITY_MEDIUM, 'Medium'), (PRIORITY_HIGH,'High')]

    STATUS_PENDING = 'pending'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = [(STATUS_PENDING, 'Pending'), (STATUS_COMPLETED, 'Completed')]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateTimeField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default=PRIORITY_MEDIUM )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_PENDING)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  
    class Meta:
        ordering = ['-due_date', '-priority']  


    def save(self, *args, **kwargs):

        #making sure due date is in the future
        if self.due_date and self.due_date <= timezone.now():
            raise ValidationError ('Due Date must bbe in the future')

        #timestamp for completeion
        if self.status == self.STATUS_COMPLETED and not self.completed_at:
            self.completed_at = timezone.now()
        elif self.status == self.STATUS_PENDING:
            self.completed_at = None
        super().save(*args, **kwargs)

try:
    #notification message
    if self.status != self.STATUS_COMPLETED and self.is_due_soon():
        Notification.objects.get_or_create(
            user=self.owner,
            task=self,
            defaults={'message': f"Your Task '{self.title}' is due in one day!!!"}
        )
except Exception:
    pass

#mark completion
    def mark_as_completed(self):
        self.status = self.STATUS_COMPLETED
        self.save()

#check status
    def check_status(self):
        if self.status == self.STATUS_COMPLETED:
            self.mark_as_completed()
        else:
            self.status = self.STATUS_PENDING
            self.save()

    def is_due_soon(self):
        #checks if due date is within a day
        if not self.due_date:
            return False  #if its completed or not close to deadline or none

        now = timezone.now()
        one_day_from_now = now + timedelta(days=1)
        #due soon
        return now < self.due_date <= one_day_from_now

    def __str__(self):
        return f"{self.title} ({self.priority}) - {self.status}"

#users
class UserManager(BaseUserManager):
    #user model manager
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email field must be set.')
        if not username:
            raise ValueError('Username field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise ValueError('Must have a password')

        user =self.create_user(username=username, email=email, password=password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    #user model
    username = models.CharField(max_length=55, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=99)
    last_name = models.CharField(max_length=99)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']

    def __str__(self):
        return self.username

#notifications for incoming due date
class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Important: {self.username} {self.message}"



    














