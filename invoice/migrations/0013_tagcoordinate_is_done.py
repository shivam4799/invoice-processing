# Generated by Django 3.1 on 2020-08-19 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0012_auto_20200819_1452'),
    ]

    operations = [
        migrations.AddField(
            model_name='tagcoordinate',
            name='is_done',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
