# Generated by Django 5.0.7 on 2024-08-06 11:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PushNotification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime.now),
            preserve_default=False,
        ),
    ]
