# Generated by Django 5.1.7 on 2025-04-13 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_saved_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(default='avatars/default.jpg', upload_to='avatars/'),
        ),
    ]
