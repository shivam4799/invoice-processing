from django.db import models
from django.urls import reverse


class Invoice(models.Model):
    # document = models.OneToOneField(Document,on_delete=models.CASCADE,primary_key=False,null=True,blank=True)
    invoice_no = models.CharField(max_length=256,null=True,blank=True)
    invoice_date = models.DateTimeField(null=True,blank=True)
    gstin = models.CharField(max_length=256,null=True,blank=True)
    cgst = models.FloatField(null=True,blank=True)
    sgst = models.FloatField(null=True,blank=True)
    igst = models.FloatField(null=True,blank=True)
    total_taxable_amount = models.FloatField(null=True,blank=True)
    total_amount = models.FloatField(null=True,blank=True)
    vendor_name = models.CharField(max_length=256,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    phone_number = models.PositiveIntegerField(null=True,blank=True)
    imei = models.PositiveIntegerField(null=True,blank=True)
    vendor_address = models.CharField(max_length=256,null=True,blank=True)
    status = models.BooleanField(null=True,blank=True)
    created_by = models.CharField(max_length=256,null=True,blank=True)
    additional_data = models.CharField(max_length=10000,null=True,blank=True,default="")


class Document(models.Model):
    pdf_copy = models.FileField(upload_to='', null=True, blank=True)
    invoice = models.OneToOneField(Invoice,on_delete=models.CASCADE,null=True,blank=True)
    # tagging_done = models.BooleanField(default=False)
    form_input_done = models.BooleanField(default=False)
    created_by = models.CharField(max_length=256,null=True,blank=True)
    last_modified_by_id = models.CharField(max_length=256,null=True,blank=True)
    last_modified_by_name = models.CharField(max_length=256,null=True,blank=True)
    last_modified = models.DateTimeField(auto_now_add=True,null=True)
    autofill_done = models.BooleanField(default=False)


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
    is_done = models.BooleanField(default=False,blank=True,null=True)
    page_id = models.PositiveIntegerField()


class BulkDocument(models.Model):
  file = models.FileField('Document', upload_to='mydocs/')


class UploadPdf(models.Model):
    file = models.FileField(upload_to='mydocs', blank=True, null=True)