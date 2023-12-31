# Generated by Django 4.2.3 on 2023-07-29 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customer_engine', '0003_delete_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('father', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('activity_level', models.CharField(max_length=50)),
                ('tall', models.DecimalField(decimal_places=1, max_digits=3)),
                ('weight', models.DecimalField(decimal_places=1, max_digits=5)),
                ('target_weight', models.DecimalField(decimal_places=1, max_digits=5)),
                ('medical_condition', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('languages', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=10)),
                ('status', models.CharField(max_length=100)),
                ('contact_number', models.CharField(max_length=15)),
                ('date', models.DateField()),
            ],
        ),
    ]
