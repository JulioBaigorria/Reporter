# Generated by Django 3.2.4 on 2021-06-08 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sale', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='total_price',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
