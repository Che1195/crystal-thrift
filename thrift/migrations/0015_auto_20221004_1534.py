# Generated by Django 3.2.15 on 2022-10-04 19:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0014_userprofile_contact_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='building',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='floor',
        ),
    ]
