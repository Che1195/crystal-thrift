# Generated by Django 3.2.15 on 2022-09-01 14:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0008_auto_20220901_1047'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='name',
            new_name='title',
        ),
    ]
