# Generated by Django 5.0.7 on 2024-08-07 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PushNotification', '0002_notification_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='FCMToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
