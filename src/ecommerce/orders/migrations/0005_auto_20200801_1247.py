# Generated by Django 3.0.8 on 2020-08-01 17:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_merge_20200801_1244'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.RemoveField(
            model_name='order',
            name='billing_address_final',
        ),
        migrations.RemoveField(
            model_name='order',
            name='shipping_address_final',
        ),
        migrations.RemoveField(
            model_name='order',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated',
        ),
        migrations.DeleteModel(
            name='ProductPurchase',
        ),
    ]
