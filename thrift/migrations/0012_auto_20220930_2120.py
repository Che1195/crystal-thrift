# Generated by Django 3.2.15 on 2022-10-01 01:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0011_auto_20220930_1927'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image1',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='item',
            name='image2',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='item',
            name='image3',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='item',
            name='image4',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='item',
            name='image5',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
