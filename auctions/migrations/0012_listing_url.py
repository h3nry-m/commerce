# Generated by Django 3.0.3 on 2021-01-29 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_remove_bid_datefield'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='url',
            field=models.CharField(default='None', max_length=200),
        ),
    ]