# Generated by Django 2.1.5 on 2019-06-06 17:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0008_census_area_observation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveychart',
            name='census_areas',
            field=models.ManyToManyField(blank=True, to='surveys.CensusArea'),
        ),
    ]
