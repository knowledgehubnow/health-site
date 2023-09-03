# Generated by Django 4.2.3 on 2023-09-03 04:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0036_calorycount_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dishes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food', models.CharField(blank=True, max_length=200, null=True)),
                ('quantity', models.CharField(max_length=10, null=True)),
                ('ingredients', models.CharField(blank=True, max_length=255, null=True)),
                ('veg_nonveg_egg', models.CharField(blank=True, max_length=255, null=True)),
                ('pral', models.FloatField(null=True)),
                ('oil', models.FloatField(null=True)),
                ('gl', models.FloatField(null=True)),
                ('cals', models.FloatField(null=True)),
                ('aaf_adj_prot', models.FloatField(null=True)),
                ('carbs', models.FloatField(null=True)),
                ('total_fat', models.FloatField(null=True)),
                ('tdf', models.FloatField(null=True)),
                ('sodium', models.FloatField(null=True)),
                ('potassium', models.FloatField(null=True)),
                ('phasphorous', models.FloatField(null=True)),
                ('calcium', models.FloatField(null=True)),
                ('magnecium', models.FloatField(null=True)),
                ('total_eaa', models.FloatField(null=True)),
                ('lysine', models.FloatField(null=True)),
                ('gross_protine', models.FloatField(null=True)),
                ('free_suger', models.FloatField(null=True)),
                ('aa_factor', models.FloatField(null=True)),
                ('glucose', models.FloatField(null=True)),
            ],
        ),
    ]