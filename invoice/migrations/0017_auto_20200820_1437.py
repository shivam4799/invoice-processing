# Generated by Django 3.1 on 2020-08-20 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0016_auto_20200820_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invoice',
            name='document',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='invoice.document'),
        ),
    ]