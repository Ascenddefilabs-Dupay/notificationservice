# Generated by Django 5.1 on 2024-09-03 05:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('special_offers', '0003_alter_adminspecialoffers_table'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='specialoffersnotifications',
            name='unique_user_notifications',
        ),
    ]
