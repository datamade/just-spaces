import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


def create_philadelphia(apps, schema_editor):
    CensusRegion = apps.get_model('surveys', 'CensusRegion')
    CensusRegion.objects.get_or_create(
        name='Philadelphia',
        slug='philadelphia',
        fips_codes=['42101']
    )


class Migration(migrations.Migration):

    dependencies = [
        ('surveys', '0016_census_area_agency'),
    ]

    operations = [
        migrations.CreateModel(
            name='CensusRegion',
            fields=[
                ('fips_codes', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=12), size=None)),
                ('slug', models.SlugField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.RunPython(create_philadelphia, reverse_code=migrations.RunPython.noop),
        migrations.AddField(
            model_name='censusblockgroup',
            name='region',
            field=models.ForeignKey(default='philadelphia', on_delete=django.db.models.deletion.PROTECT, to='surveys.CensusRegion'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='censusarea',
            name='region',
            field=models.ForeignKey(default='philadelphia', on_delete=django.db.models.deletion.PROTECT, to='surveys.CensusRegion'),
            preserve_default=False,
        ),
    ]
