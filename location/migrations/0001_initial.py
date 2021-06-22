# Generated by Django 3.2.4 on 2021-06-22 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(default='', max_length=100)),
                ('location_code', models.CharField(default='', max_length=100)),
                ('location_hfr_code', models.CharField(default='', max_length=100)),
                ('location_level', models.PositiveIntegerField(choices=[(0, 'Nation'), (1, 'Region'), (2, 'Council')], default=0)),
                ('location_reference', models.CharField(max_length=150)),
            ],
        ),
    ]
