# Generated by Django 4.2.7 on 2023-11-22 06:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0003_remove_food_address_remove_food_tg_username_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='food',
            options={'ordering': ['-id']},
        ),
    ]
