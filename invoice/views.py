from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import CreateView,ListView,TemplateView,DetailView,View,DeleteView,UpdateView
from .models import *
from .forms import *
import json
import base64
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
import requests
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
import os
from autoshift.settings import PDF_FILES,PROJECT_ROOT,BASE_DIR
from pathlib import Path
import img2pdf
from PIL import Image


class CreateForm(LoginRequiredMixin,CreateView):
    login_url = '/auth/'
    template_name = 'invoice-create.html'
    form_class = InvoicesForm

    def get_context_data(self,**kwargs):
        print('in get context data')
        data = super(CreateForm,self).get_context_data(**kwargs)
        try:
            path_file = Document.objects.filter().last()
            pdf_file = str(path_file.pdf_copy).split('.')[0] + '.pdf'
            print(pdf_file)
            data['pdf_file'] = pdf_file
            path = str(Path(PROJECT_ROOT)) + str(Path(str(path_file.pdf_copy)))
            path = os.path.normpath(path)
            print('final', path)
        except:
            data['pdf_file'] = None
        return data

    def form_valid(self,form):
        self.object = form.save()
        print('after saving ')
        print(self.request.POST)
        form.instance.created_by = 'agent123'
        if self.request.POST.get('additional_data'):
            resp = json.loads(self.request.POST.get('additional_data'))
            invoice_id = resp['invoice_id']
            annotation_values = resp['annotation_values']
            item_values = resp['item_values']

            for annot in annotation_values:
                inner_value = annot['vals'].split(':')[1].split(',')
                annotation_tag = annot['global_tag_id']
                pagenum = annot['pagenum']
                hmin = float(inner_value[0])
                hmax = float(inner_value[1])
                wmin = float(inner_value[2])
                wmax = float(inner_value[3])
                TagCoordinate(invoice=self.object,annotation=annotation_tag, hmin=hmin, hmax=hmax, wmin=wmin, wmax=wmax, page_id=pagenum).save()

            for item in item_values:
                Item(invoice=self.object,item_quantity=(item['item_q']),item_rate=(item['item_r']),item_description=(item['item_d'])).save()

        return super(CreateForm, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('create')


class InvoiceList(LoginRequiredMixin,ListView):
    login_url = '/auth/'
    template_name = 'Dashboard.html'
    model = Invoice
    context_object_name = 'invoices'


class InvoiceDetailView(LoginRequiredMixin,DetailView):
    login_url = '/auth/'
    model = Invoice
    template_name = 'invoice-detail.html'
    context_object_name = 'invoices_details'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        return context


class InvoiceDeleteView(DeleteView,LoginRequiredMixin):
    model = Invoice
    template_name = 'invoice-delete.html'
    success_url = reverse_lazy('home')


class InvoiceUpdateView(UpdateView,LoginRequiredMixin):
    model = Invoice
    template_name = 'invoice-create.html'
    form_class = InvoicesForm

    def get_context_data(self, **kwargs):
        print('in get context data')
        data = super(InvoiceUpdateView,self).get_context_data(**kwargs)
        path_file = Document.objects.filter().last()
        data['items'] = Item.objects.filter(invoice=self.object)
        print(data['items'])
        pdf_file = str(path_file.pdf_copy).split('.')[0] +'.pdf'
        print(pdf_file)
        data['pdf_file'] = pdf_file
        return data

    def form_valid(self, form):
        self.object = form.save()
        print('after saving ')
        print(self.request.POST)
        form.instance.created_by = 'agent123'
        additional_data = self.request.POST.get('additional_data')
        if additional_data:
            resp = json.loads(additional_data)
            # invoice_id = resp['invoice_id']
            annotation_values = resp['annotation_values']
            item_values = resp['item_values']

            for annot in resp['annotation_values']:
                inner_value = annot['vals'].split(':')[1].split(',')
                annotation_tag = annot['global_tag_id']
                pagenum = annot['pagenum']
                hmin = float(inner_value[0])
                hmax = float(inner_value[1])
                wmin = float(inner_value[2])
                wmax = float(inner_value[3])
                TagCoordinate(invoice=self.object, annotation=annotation_tag, hmin=hmin, hmax=hmax, wmin=wmin,
                              wmax=wmax, page_id=pagenum).save()

            for item in item_values:
                Item(invoice=self.object, item_quantity=(item['item_q']), item_rate=(item['item_r']),
                     item_description=(item['item_d'])).save()

        return super(CreateForm, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('create')


class BillingPage(TemplateView,LoginRequiredMixin):
    template_name = 'billing.html'


class SettingsPage(TemplateView,LoginRequiredMixin):
    template_name = 'settings_profile.html'


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']

        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        doc = Document(pdf_copy=url)
        doc.save()

        try:
            path_file = Document.objects.filter().last()

            path = str(Path(PROJECT_ROOT)) + str(Path(str(path_file.pdf_copy)))
            path = os.path.normpath(path)

            img_path = path

            pdf_path = (path.split('.'))[0]+'.pdf'

            image = Image.open(img_path)
            pdf_bytes = img2pdf.convert(image.filename)

            file = open(pdf_path, "wb")
            file.write(pdf_bytes)

            image.close()

            print('filename ',str(uploaded_file.name).split('.')[0])
            print('file path name',file.name)
            doc = Document(pdf_copy=url)
            doc.save()

            file.close()

            # image field

            print("Successfully made pdf file")

        except:
            pass


        return redirect('/create')
    else:
        return redirect('/create')


class Demo(TemplateView):
    template_name = 'invoice-preview.html'


class Testing(TemplateView):
    template_name = 'trail.html'


def api_call(request):
    context = {}
    path_file = Document.objects.filter().last()
    pdf_file = str(path_file.pdf_copy).split('.')[0] + '.pdf'
    print(pdf_file)
    context['pdf_file'] = pdf_file

    form = InvoicesForm()

    url = "https://process-workorder-sync-55eyzztxca-uc.a.run.app"

    path = str(Path(PROJECT_ROOT)) + str(Path(str(path_file.pdf_copy)))
    path = os.path.normpath(path)

    payload = {'user_id': '123'}

    files = [
        ('file', open(str(path), 'rb'))
    ]

    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    response = response.json()
    response = response['data']
    # print(response)

    invoice_number = response['invoice_number']
    invoice_date = response['invoice_date']
    gstin = response['vendor_gstin']
    print('gstin',gstin[0]['value'])
    vendor_address = response['state_code']
    total_amount = response['total_amount']
    sgst = response['sgsts']
    cgst = response['cgsts']
    igst = response['igsts']

    total_taxable_amount = response['total_taxable_amount']

    if invoice_number:
        form.fields['invoice_no'].initial = invoice_number[0]['value']
    if invoice_date:
        form.fields['invoice_date'].initial = invoice_date[0]['value']
    if gstin:
        form.fields['gstin'].initial = gstin[0]['value']
    if total_amount:
        form.fields['total_amount'].initial = total_amount[0]['value']
    if sgst:
        form.fields['sgst'].initial = sgst[0]['value']
    if cgst:
        form.fields['cgst'].initial = cgst[0]['value']
    if igst:
        form.fields['igst'].initial = igst[0]['value']
    if total_taxable_amount:
        form.fields['total_taxable_amount'].initial = total_taxable_amount[0]['value']

    context['form'] = form

    return render(request,'invoice-create.html',context=context)


def logout(request):
    auth.logout(request)
    if not request.user.is_authenticated:
        print('Not logged in')
    return redirect('/auth/')