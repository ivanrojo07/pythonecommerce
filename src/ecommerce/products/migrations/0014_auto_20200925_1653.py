# Generated by Django 3.1.1 on 2020-09-25 21:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_auto_20200924_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='productfile',
            name='free',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='productfile',
            name='user_required',
            field=models.BooleanField(default=False),
        ),
    ]
