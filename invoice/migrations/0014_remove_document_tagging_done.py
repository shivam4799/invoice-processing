# Generated by Django 3.1 on 2020-08-19 10:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0013_tagcoordinate_is_done'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='tagging_done',
        ),
    ]
