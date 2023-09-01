# Generated by Django 4.2.3 on 2023-09-01 01:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0034_rename_launch_lunch'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaloryCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('calory', models.FloatField(default=0.0)),
                ('total_calory', models.FloatField(default=0.0)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer_engine.customer')),
            ],
        ),
    ]
