# Generated by Django 4.1.4 on 2023-01-07 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myblog', '0005_post_dislikes_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='dislikes',
        ),
        migrations.RemoveField(
            model_name='post',
            name='likes',
        ),
    ]
