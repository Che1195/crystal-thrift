# Generated by Django 3.2.15 on 2022-08-16 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_userprofile_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
