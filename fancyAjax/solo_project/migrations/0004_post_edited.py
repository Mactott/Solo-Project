# Generated by Django 2.2.4 on 2023-08-05 19:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solo_project', '0003_post_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='edited',
            field=models.BooleanField(default=False),
        ),
    ]
