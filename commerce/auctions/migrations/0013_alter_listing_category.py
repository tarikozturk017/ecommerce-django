# Generated by Django 4.1.1 on 2022-10-19 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_listing_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Clothing', 'Clothing'), ('Furniture', 'Furniture'), ('Electronics', 'Electronics'), ('Kitchen', 'Kitchen'), ('Pets', 'Pets'), ('Sport', 'Sport'), ('Vehicles', 'Vehicles'), ('Artwork', 'Artwork'), ('Others', 'Others')], default='Sport', max_length=64),
        ),
    ]
