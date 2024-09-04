# Generated by Django 5.1 on 2024-09-04 06:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminProductAnnouncement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'admin_product_announcement',
            },
        ),
        migrations.CreateModel(
            name='ProductAnnouncementNotifications',
            fields=[
                ('notification_id', models.CharField(editable=False, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('user_id', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'product_announcement_notifications',
            },
        ),
    ]
