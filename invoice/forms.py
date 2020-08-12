from django import forms
from .models import *


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class InvoicesForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('created_by',)

        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'invoice_no_input',},),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'invoice_date_input'}),
            'gstin': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'gstin_input'}),
            'vendor_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'vendor_name_input'}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'email_input'}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'phone_number_input'}),
            'imei': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'imei_input'}),
            'vendor_address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True,'id':'vendor_address_input'}),
            'total_taxable_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'vendor_address_input'}),
            'sgst': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'vendor_address_input'}),
            'igst': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'vendor_address_input'}),
            'cgst': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'vendor_address_input'}),
            'total_amount': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True, 'id': 'vendor_address_input'}),
            'additional_data':forms.TextInput(attrs={'style':'display:none','id':'ad-id'})
            }
