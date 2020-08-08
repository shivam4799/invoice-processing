from django.db import models


# Create your models here.
class Invoice(models.Model):
    invoice_no = models.PositiveIntegerField()
    invoice_date = models.DateTimeField()
    gstin = models.PositiveIntegerField()
    vendor_name = models.PositiveIntegerField()
    email = models.EmailField()
    phone_number = models.PositiveIntegerField()
    imei = models.PositiveIntegerField()
    vendor_address = models.CharField(max_length=256)
    status = models.BooleanField()


class Document(models.Model):
    pdf_copy = models.FileField(upload_to='', null=True, blank=True)


class Item(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='invoice',on_delete=models.CASCADE)
    item_quantity = models.FloatField()
    item_rate = models.FloatField()
    item_description = models.CharField(max_length=256)


class TempItem(models.Model):
    # invoice = models.ForeignKey(Invoice, related_name='temp_invoice', on_delete=models.CASCADE)
    item_q = models.FloatField()
    item_r = models.FloatField()
    item_d = models.CharField(max_length=256)


class TagCoordinate(models.Model):
    annotation = models.CharField(max_length=256)
    # field named type ( choice field )
    hmin = models.FloatField()
    wmin = models.FloatField()
    hmax = models.FloatField()
    wmax = models.FloatField()
    page_id = models.PositiveIntegerField()
