# Generated by Django 3.1.1 on 2020-09-25 00:11

import django.core.files.storage
from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_productfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productfile',
            name='file',
            field=models.FileField(storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\ivanr\\Documents\\pythonecommerce\\src\\static_cdn\\protected_media'), upload_to=products.models.upload_product_file_loc),
        ),
    ]
