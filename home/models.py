from django.db import models
from django.contrib.auth.models import User
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

class CodeSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='code_sessions')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class CodeMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('system', 'System'),
    )
    session = models.ForeignKey(CodeSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}"

class StudySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='study_sessions')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.user.username}"

class StudyMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('system', 'System'),
    )
    session = models.ForeignKey(StudySession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}"

class WorksheetSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='worksheet_sessions')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class WorksheetMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('system', 'System'),
    )
    session = models.ForeignKey(WorksheetSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}"
    
class ResearchSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='research_sessions')
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class ResearchMessage(models.Model):
    SENDER_CHOICES = (
        ('user', 'User'),
        ('system', 'System'),
    )
    session = models.ForeignKey(ResearchSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=20, choices=SENDER_CHOICES)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} @ {self.timestamp}"