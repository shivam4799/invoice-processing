# Generated by Django 3.1 on 2020-08-19 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0011_document_autofill_done'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='last_modified_by',
            new_name='last_modified_by_id',
        ),
        migrations.AddField(
            model_name='document',
            name='last_modified_by_name',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]