from django.db import models
from django.utils.timezone import now

class ContactMessage(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class Policy(models.Model):
    POLICY_TYPES = [
        ('tos', 'Terms of Service'),
        ('privacy', 'Privacy Policy'),
        ('cookies', 'Cookies Policy'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    policy_type = models.CharField(max_length=10, choices=POLICY_TYPES, unique=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
