# Generated by Django 3.2.4 on 2021-06-19 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Sale', '0005_alter_position_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
