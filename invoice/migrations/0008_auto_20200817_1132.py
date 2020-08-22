# Generated by Django 3.1 on 2020-08-17 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0007_bulkdocument_uploadpdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='created_by',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='form_input_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='document',
            name='tagging_done',
            field=models.BooleanField(default=False),
        ),
    ]
