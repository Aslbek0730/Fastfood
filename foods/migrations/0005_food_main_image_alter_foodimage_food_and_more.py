# Generated by Django 5.1.7 on 2025-04-13 09:32

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0004_alter_food_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='main_image',
            field=models.ImageField(default='food_images/default.jpg', upload_to='food_images'),
        ),
        migrations.AlterField(
            model_name='foodimage',
            name='food',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='foods.food'),
        ),
        migrations.AlterField(
            model_name='foodimage',
            name='image',
            field=models.ImageField(help_text='Allowed formats: jpg, jpeg, png, gif', upload_to='food_images', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]),
        ),
    ]
