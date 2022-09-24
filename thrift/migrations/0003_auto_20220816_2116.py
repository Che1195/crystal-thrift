# Generated by Django 3.2.15 on 2022-08-17 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0002_auto_20220816_2104'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='publish',
        ),
        migrations.RemoveField(
            model_name='item',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='item',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='publish',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='updated',
        ),
        migrations.AddField(
            model_name='item',
            name='created',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='modified',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='modified',
            field=models.DateTimeField(null=True),
        ),
    ]