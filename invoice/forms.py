from django import forms
from .models import *
from django.forms import ClearableFileInput


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class InvoicesForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('created_by',)

        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id':'invoice_no_input',},),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'id':'invoice_date_input'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id':'gstin_input'}),
            'vendor_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id':'vendor_name_input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'id':'email_input'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id':'phone_number_input'}),
            'imei': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'id':'imei_input'}),
            'vendor_address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'id':'vendor_address_input'}),
            'total_taxable_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'id': 'total_taxable_amount_input'}),
            'sgst': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'id': 'sgst_input'}),
            'igst': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'id': 'igst_input'}),
            'cgst': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'id': 'cgst_input'}),
            'total_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm',  'id': 'total_amount_input'}),
            'additional_data':forms.TextInput(attrs={'style':'display:none','id':'ad-id'})
            }


class ResumeUpload(forms.ModelForm):
    class Meta:
        model = UploadPdf
        fields = ['file']
        widgets = {
            'file': ClearableFileInput(attrs={'multiple': True}),
        }