# Generated by Django 5.1.6 on 2025-02-27 00:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudySession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_activity', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='study_sessions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StudyMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender', models.CharField(choices=[('user', 'User'), ('system', 'System')], max_length=20)),
                ('text', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='home.studysession')),
            ],
        ),
    ]
