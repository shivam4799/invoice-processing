from django.db import models


# Create your models here.
class Invoice(models.Model):
    invoice_no = models.CharField(max_length=256)
    invoice_date = models.DateTimeField()
    gstin = models.PositiveIntegerField()
    cgst = models.PositiveIntegerField(null=True,blank=True)
    sgst = models.PositiveIntegerField(null=True,blank=True)
    igst = models.PositiveIntegerField(null=True,blank=True)
    total_taxable_amount = models.PositiveIntegerField()
    total_amount = models.PositiveIntegerField()
    vendor_name = models.CharField(max_length=256)
    email = models.EmailField()
    phone_number = models.PositiveIntegerField()
    imei = models.PositiveIntegerField()
    vendor_address = models.CharField(max_length=256)
    status = models.BooleanField(null=True,blank=True)
    created_by = models.CharField(max_length=256)
    additional_data = models.CharField(max_length=10000,null=True,blank=True,default="")


class Document(models.Model):
    pdf_copy = models.FileField(upload_to='', null=True, blank=True)


class Item(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='invoice',on_delete=models.CASCADE)
    item_quantity = models.FloatField()
    item_rate = models.FloatField()
    item_description = models.CharField(max_length=256)


class TagCoordinate(models.Model):
    invoice = models.ForeignKey(Invoice,related_name='invoice_Tag',on_delete=models.CASCADE)
    document = models.ForeignKey(Document,on_delete=models.SET_NULL,null=True)
    annotation = models.CharField(max_length=256)
    # field named type ( choice field )
    TYPE_CHOICES = (
        ('image','image'),
        ('text','text')
    )
    annotation_type = models.CharField(max_length=20,choices=TYPE_CHOICES,default='image',blank=True,null=True)
    hmin = models.FloatField()
    wmin = models.FloatField()
    hmax = models.FloatField()
    wmax = models.FloatField()
    page_id = models.PositiveIntegerField()
