# Generated by Django 5.0.6 on 2024-06-21 04:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_course_options_alter_lesson_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usernotification',
            name='user',
        ),
    ]