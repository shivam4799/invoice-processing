from django.forms import ModelForm
from django import forms
from .models import *
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, HTML, ButtonHolder, Submit
from .custom_layout_object import *
#collection -- invoice
#collectiontitle -- items


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ()
        widgets = {
            'invoice_date': forms.DateInput()
        }


ItemFormSet = inlineformset_factory(
    Invoice, Item, form=ItemForm,
    fields='__all__', extra=2, can_delete=True
    )


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = '__all__'


class InvoicesForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('status',)

        widgets = {
            'invoice_no': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'invoice_date': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'gstin': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'vendor_name': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'email': forms.EmailInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'phone_number': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'imei': forms.NumberInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            'vendor_address': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'required': True}),
            # 'status': forms.BooleanField(attrs={'class':'form-control form-control-sm','required':True})
        }

#
# class TempItemForm(forms.ModelForm):
#
#     class Meta:
#         model = TempItem
#         fields = '__all__'
#
#         widgets = {
#             'item_description':forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
#             'item_quantity':forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
#             'item_rate':forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True})
#         }


class InvoiceForm(forms.ModelForm):

    class Meta:
        model = Invoice
        exclude = ('status',)
        # fields = '__all__'

        widgets = {
            'invoice_no': forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'invoice_date': forms.DateInput(attrs={'class':'form-control form-control-sm','required':True}),
            'gstin': forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
            'vendor_name': forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            'email': forms.EmailInput(attrs={'class':'form-control form-control-sm','required':True}),
            'phone_number': forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
            'imei': forms.NumberInput(attrs={'class':'form-control form-control-sm','required':True}),
            'vendor_address': forms.TextInput(attrs={'class':'form-control form-control-sm','required':True}),
            # 'status': forms.BooleanField(attrs={'class':'form-control form-control-sm','required':True})
        }

    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3 create-label'
        self.helper.field_class = 'input-group sm-3'
        self.helper.layout = Layout(
            Div(
                #Field('invoice_no'),
                #Field('invoice_date'),
                #Field('vendor_name'),
                #Field('email'),
                Fieldset('Add Items',
                   Formset('titles')),
                HTML("<br>"),
                ButtonHolder(Submit('submit', 'Save')),

                )
            )