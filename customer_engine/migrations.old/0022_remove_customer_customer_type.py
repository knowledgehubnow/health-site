# Generated by Django 4.2.3 on 2023-08-11 15:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0021_customer_height_unit_customer_weight_unit_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_type',
        ),
    ]