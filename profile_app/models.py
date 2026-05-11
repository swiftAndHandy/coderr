from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to='uploads/profiles/', blank=True)
    location = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    working_hours = models.CharField(max_length=100, blank=True)
    type = models.CharField(max_length=100, choices=[
        ('business', 'Business'),
        ('customer', 'Customer')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
