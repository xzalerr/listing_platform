# Generated by Django 5.2 on 2025-06-08 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0005_alter_listing_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.ImageField(blank=True, default='media/database_error.jpg', upload_to='main_images/'),
        ),
    ]
