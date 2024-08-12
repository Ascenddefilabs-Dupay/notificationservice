# Generated by Django 5.0.7 on 2024-08-12 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EmailVerificationNotification',
            fields=[
                ('notification_id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(blank=True, max_length=255, null=True)),
                ('email_id', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('type', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'notification',
            },
        ),
    ]