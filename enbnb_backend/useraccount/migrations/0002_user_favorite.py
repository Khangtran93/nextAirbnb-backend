# Generated by Django 5.1 on 2025-03-06 03:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0007_propertyimage_upload_at'),
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorite',
            field=models.ManyToManyField(blank=True, related_name='favorite_by', to='property.property'),
        ),
    ]
