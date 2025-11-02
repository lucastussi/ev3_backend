from django.db import models
from django.contrib.auth.models import User

class Asset(models.Model):
    CRITICALITY_CHOICES = [
        ('low', 'Low'),
        ('med', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    criticality = models.CharField(max_length=10, choices=CRITICALITY_CHOICES, default='low')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name