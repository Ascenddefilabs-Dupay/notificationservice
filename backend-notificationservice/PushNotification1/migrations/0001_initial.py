# Generated by Django 5.1 on 2024-10-03 05:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminMessages',
            fields=[
                ('content_id', models.CharField(editable=False, max_length=6, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.localtime)),
            ],
            options={
                'db_table': 'admin_messages',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='MessagesNotifications',
            fields=[
                ('notification_id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'messages_notifications',
            },
        ),
        migrations.CreateModel(
            name='NotificationSettings',
            fields=[
                ('user_id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('messages', models.BooleanField(default=True)),
                ('product_announcement', models.BooleanField(default=True)),
                ('special_offers', models.BooleanField(default=True)),
                ('insights_tips', models.BooleanField(default=True)),
                ('price_alerts', models.BooleanField(default=True)),
                ('account_activity', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'notification_settings',
            },
        ),
    ]
