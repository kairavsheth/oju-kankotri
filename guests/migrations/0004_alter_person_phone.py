# Generated by Django 4.1 on 2022-08-13 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0003_alter_person_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='phone',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]