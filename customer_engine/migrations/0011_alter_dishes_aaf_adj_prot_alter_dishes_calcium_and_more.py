# Generated by Django 4.2.3 on 2023-07-31 07:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_engine', '0010_alter_dishes_aaf_adj_prot_alter_dishes_calcium_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dishes',
            name='aaf_adj_prot',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='calcium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='calories',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='carbohydtrates',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='food',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='free_suger',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='glycemicload',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='gross_protine',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='lysine',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='magnecium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='oil',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='phasphorous',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='potassium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='pral',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='quantity',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='sodium',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='tdf',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='total_eaa',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='dishes',
            name='total_fat',
            field=models.FloatField(null=True),
        ),
    ]
