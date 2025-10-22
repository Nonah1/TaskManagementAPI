from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

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
  
    class Meta:
        ordering = ['-due_date', '-priority']  

    def save(self):
        if self.status == self.STATUS_COMPLETED and not self.conmpleted_at:
            self.completed_at = timezone.now()
        if self.status == self.STATUS_PENDING:
            self.completed_at = None
        super().save()

#making sure due date is in the future
    def clean(self):
        if self.due_date <= datetime.now():
            raise ValidationError({'due_date' : 'Due Date must bbe in the future'})

    def __str__(self):
        return f"{'self.title'} ({self.priority}) - {self.status}"

#for adding the fields and attributes
class CustomUser(AbstractUser):
    email = models.EmailField(('emailaddress'), unique=True)

    def __str__(self):
        return self.email

    














