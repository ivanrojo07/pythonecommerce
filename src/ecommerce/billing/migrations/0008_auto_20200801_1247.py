# Generated by Django 3.0.8 on 2020-08-01 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0007_auto_20171012_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='charge',
            name='billing_profile',
        ),
        migrations.RemoveField(
            model_name='billingprofile',
            name='customer_id',
        ),
        migrations.DeleteModel(
            name='Card',
        ),
        migrations.DeleteModel(
            name='Charge',
        ),
    ]