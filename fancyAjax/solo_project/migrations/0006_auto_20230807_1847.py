# Generated by Django 2.2.4 on 2023-08-08 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solo_project', '0005_post_updated_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='first_name',
            new_name='username',
        ),
        migrations.RemoveField(
            model_name='user',
            name='last_name',
        ),
    ]
