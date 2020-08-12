# Generated by Django 3.1 on 2020-08-11 05:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_copy', models.FileField(blank=True, null=True, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invoice_no', models.CharField(max_length=256)),
                ('invoice_date', models.DateTimeField()),
                ('gstin', models.PositiveIntegerField()),
                ('vendor_name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.PositiveIntegerField()),
                ('imei', models.PositiveIntegerField()),
                ('vendor_address', models.CharField(max_length=256)),
                ('status', models.BooleanField(blank=True, null=True)),
                ('additional_data', models.CharField(blank=True, default='', max_length=10000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TagCoordinate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annotation', models.CharField(max_length=256)),
                ('annotation_type', models.CharField(blank=True, choices=[('image', 'image'), ('text', 'text')], default='image', max_length=20, null=True)),
                ('hmin', models.FloatField()),
                ('wmin', models.FloatField()),
                ('hmax', models.FloatField()),
                ('wmax', models.FloatField()),
                ('page_id', models.PositiveIntegerField()),
                ('document', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='invoice.document')),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice_Tag', to='invoice.invoice')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_quantity', models.FloatField()),
                ('item_rate', models.FloatField()),
                ('item_description', models.CharField(max_length=256)),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoice', to='invoice.invoice')),
            ],
        ),
    ]
