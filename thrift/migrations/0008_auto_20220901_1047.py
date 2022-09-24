# Generated by Django 3.2.15 on 2022-09-01 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thrift', '0007_alter_item_date_sold'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='sold',
        ),
        migrations.AddField(
            model_name='item',
            name='sale_status',
            field=models.CharField(choices=[('available', 'available'), ('pending', 'pending'), ('sold', 'sold')], default='available', max_length=20, null=True),
        ),
    ]