# Generated by Django 3.2.15 on 2022-08-17 01:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='publish',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='publish',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='slug',
            field=models.SlugField(default=uuid.uuid4, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
