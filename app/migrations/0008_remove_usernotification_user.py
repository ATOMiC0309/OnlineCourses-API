# Generated by Django 5.0.6 on 2024-06-21 04:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_usernotification_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotification',
            name='user',
        ),
    ]
