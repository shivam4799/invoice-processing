from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import CreateView,ListView,TemplateView,DetailView,View,DeleteView,UpdateView
from .models import *
from .forms import *
import json
import datetime
from django.http.response import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import auth
import requests
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
import os
from autoshift.settings import PDF_FILES,PROJECT_ROOT,MEDIA_ROOT
from pathlib import Path
import img2pdf
from PIL import Image
from time import sleep
from django_q.tasks import async_task


class CreateForm(LoginRequiredMixin,CreateView):
    login_url = '/auth/'
    template_name = 'invoice-create.html'
    form_class = InvoicesForm

    def get_context_data(self,**kwargs):
        print('in get context data')
        data = super(CreateForm,self).get_context_data(**kwargs)
        try:
            path_file = Document.objects.get(id=self.kwargs['pk'])
            print(path_file.pdf_copy)
            data['pdf_file'] = path_file.pdf_copy
            data['docs'] = path_file
            path = str(Path(PROJECT_ROOT)) + str(Path(str(path_file.pdf_copy)))
            path = os.path.normpath(path)
        except:
            data['pdf_file'] = None
        return data

    def form_valid(self,form,*args,**kwargs):
        self.object = form.save()
        path_file = Document.objects.filter(id=self.kwargs['pk'])
        form.instance.created_by = self.request.user.id

        for p in path_file:
            form.instance.document = p
            p.last_modified_by_id = self.request.user.id
            p.last_modified_by_name = self.request.user.username
            p.last_modified = datetime.datetime.now()
            p.form_input_done = True
            p.save()
        if self.request.POST.get('additional_data'):
            resp = json.loads(self.request.POST.get('additional_data'))
            invoice_id = resp['invoice_id']
            annotation_values = resp['annotation_values']
            item_values = resp['item_values']

            for annot in annotation_values:
                inner_value = annot['vals'].split(':')[1].split(',')
                annotation_tag = annot['global_tag_id']
                pagenum = annot['pagenum']
                height = annot['height']
                width = annot['width']
                hmin = float(inner_value[0])/height
                hmax = float(inner_value[1])/height
                wmin = float(inner_value[2])/width
                wmax = float(inner_value[3])/width
                print(inner_value)
                TagCoordinate(invoice=self.object,annotation=annotation_tag, hmin=hmin, hmax=hmax, wmin=wmin, wmax=wmax, page_id=pagenum,is_done=True).save()

            for item in item_values:
                Item(invoice=self.object,item_quantity=(item['item_q']),item_rate=(item['item_r']),item_description=(item['item_d'])).save()

        return super(CreateForm, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('invoices')


def count_tagged_number(qs):
    if qs:
        count = 0
        tags = TagCoordinate.objects.filter(document=qs[0])
        for tag in tags:
            if tag.is_done:
                count += 1
            else:
                pass
        return count


class InvoiceList(LoginRequiredMixin,ListView):
    login_url = '/auth/'
    template_name = 'invoices-dashboard.html'
    model = Invoice
    context_object_name = 'invoices'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(InvoiceList, self).get_context_data(**kwargs)
        qs = Document.objects.filter(last_modified_by_id=self.request.user.id)
        context['fetched_data'] = qs
        for q in qs:
            print(q.id)
        context['count'] = count_tagged_number(qs)
        context['form'] = InvoicesForm()
        return context

    def get_queryset(self):
        qs = self.model.objects.filter(created_by=self.request.user.id)
        return qs


class InvoiceListModel(LoginRequiredMixin,ListView):
    login_url = '/auth/'
    template_name = 'Dashboard.html'
    model = Document
    context_object_name = 'docs'

    def get_context_data(self, **kwargs):
        context = super(InvoiceListModel, self).get_context_data(**kwargs)
        qs = self.model.objects.filter(created_by=self.request.user.id)

        context['form'] = InvoicesForm
        context['count'] = count_tagged_number(qs)
        context['docs'] = qs

        return context


class InvoiceDetailView(LoginRequiredMixin,DetailView):
    login_url = '/auth/'
    model = Invoice
    template_name = 'invoice-detail.html'
    context_object_name = 'invoices_details'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        return context


class InvoiceDetailTemplate(LoginRequiredMixin,TemplateView):
    login_url = '/auth/'
    model = Invoice
    template_name = 'invoice-detail.html'
    context_object_name = 'invoices'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailTemplate,self).get_context_data(**kwargs)
        context['invoice'] = self.model.objects.get(id=self.kwargs['pk'])
        return context


class InvoiceDeleteView(DeleteView,LoginRequiredMixin):
    model = Document
    template_name = 'invoice-delete.html'
    success_url = reverse_lazy('home')


class InvoiceUpdateView(LoginRequiredMixin,UpdateView):
    model = Invoice
    template_name = 'invoice-update.html'
    form_class = InvoicesForm

    def get_context_data(self, **kwargs):
        print('in get context data')
        data = super(InvoiceUpdateView,self).get_context_data(**kwargs)
        path_file = self.model.objects.get(id=self.kwargs['pk'])
        data['docs'] = path_file

        data['pdf_file'] = Document.objects.get(invoice=path_file).pdf_copy

        data['items'] = Item.objects.filter(invoice=self.object)
        print(data['pdf_file'])
        return data

    def form_valid(self, form):
        print('after saving ')

        form.instance.created_by = self.request.user.id
        additional_data = self.request.POST.get('additional_data')
        if additional_data:
            resp = json.loads(additional_data)

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

            for item in resp['item_values']:
                Item(invoice=self.object, item_quantity=(item['item_q']), item_rate=(item['item_r']),
                     item_description=(item['item_d'])).save()

        return super(InvoiceUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('home')


class BulkUploadView(LoginRequiredMixin,TemplateView):
    template_name = 'Upload_bulk.html'


def fetch(request):
    number = request.POST.get('number')

    qs = Document.objects.filter(last_modified_by_id=None).filter(autofill_done=True).order_by('-id')[:int(number)][::-1]

    for q in qs:
        q.last_modified_by_id = request.user.id
        q.last_modified_by_name = request.user.username
        q.save()

    return HttpResponseRedirect('invoices')


def removeormakenull(request,id):
    qs = Document.objects.filter(id=id)
    for q in qs:
        q.last_modified_by_id = None
        q.last_modified_by_name = None
        q.save()
    return HttpResponseRedirect('/invoices')


class BillingPage(TemplateView,LoginRequiredMixin):
    template_name = 'billing.html'


class SettingsPage(TemplateView,LoginRequiredMixin):
    template_name = 'settings_profile.html'


def autofill_async(id):
    form = InvoicesForm()

    doc = Document.objects.get(id=id)

    url = "https://process-workorder-sync-55eyzztxca-uc.a.run.app"

    path = str(Path(PROJECT_ROOT)) + str(Path(str(doc.pdf_copy)))
    path = os.path.normpath(path)

    payload = {'user_id': '123'}

    files = [
        ('file', open(str(path), 'rb'))
    ]


    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    response = response.json()['data']

    print(response)

    invoice_number = response['invoice_number']
    invoice_date = response['invoice_date']
    gstin = response['vendor_gstin']
    vendor_address = response['state_code']
    total_amount = response['total_amount']
    imei = response['imei']
    sgst = response['sgsts']
    cgst = response['cgsts']
    igst = response['igsts']
    total_taxable_amount = response['total_taxable_amount']

    invoice_date[0]['value'] = datetime.datetime.strptime(invoice_date[0]['value'], '%d/%m/%Y').strftime('%Y-%m-%d')

    if invoice_number:
        form.instance.invoice_no = invoice_number[0]['value']
    if invoice_date:
        form.instance.invoice_date = invoice_date[0]['value']
    if gstin:
        form.instance.gstin = gstin[0]['value']
    if total_amount:
        form.instance.total_amount = total_amount[0]['value']
    if sgst:
        # form.instance.sgst = sgst[0]['value']
        pass
    if cgst:
        # form.instance.cgst = cgst[0]['value']
        pass
    if igst:
        # form.instance.igst = igst[0]['value']
        pass
    if total_taxable_amount:
        form.instance.total_taxable_amount = total_taxable_amount[0]['value']
    if vendor_address:
        form.instance.vendor_address = vendor_address[0]['value']
    if imei:
        form.instance.imei = imei[0]['value']

    form.instance.save()
    doc.invoice = form.instance
    print(doc.invoice)

    doc.autofill_done = True
    doc.pdf_copy = str(doc.pdf_copy).split('.')[0] + '.pdf'

    doc.save()

    print('saving form now !!')


def upload(request):
    if request.method == 'POST':
        files = request.FILES.getlist('file')
        for f in files:
            fs = FileSystemStorage()
            name = fs.save(f.name, f)
            url = fs.url(name)

            doc = Document(pdf_copy=url,created_by=request.user.id)
            doc.save()

            async_task('invoice.views.autofill_async',doc.id)

            try:
                path_file = Document.objects.filter().last()

                img_path_media = str(path_file.pdf_copy)
                pdf_path_media = (img_path_media.split('.'))[0]+'.pdf'

                img_path = str(Path(PROJECT_ROOT)) + str(Path(img_path_media))
                pdf_path = str(Path(PROJECT_ROOT)) + str(Path(pdf_path_media))

                img_path = os.path.normpath(img_path)
                pdf_path = os.path.normpath(pdf_path)

                image = Image.open(img_path)
                pdf_bytes = img2pdf.convert(image.filename)

                file = open(pdf_path, "wb")
                file.write(pdf_bytes)

                image.close()

                pdfdoc = Document(pdf_copy=pdf_path_media,created_by=request.user.id)
                # pdfdoc.save()

                # doc.delete()
                file.close()

            except:
                pass

        return redirect('/')
    else:
        return redirect('/')


def multipage_upload(request):
    print('calling api')
    url = "https://convert-img-to-pdf-mti64mke4a-uc.a.run.app"
    multipage_files = []

    files = request.FILES.getlist('image')

    for f in files:
        multipage_files.append(('file',(f.name,f,'image/jpeg')))
        print(f.name)

    payload = {}

    response = requests.request("POST",url,data=payload,files=multipage_files)
    pdf_path = str(Path(MEDIA_ROOT)) + str('/')
    print('pdf path error',pdf_path)
    pdf_path = str(pdf_path) +str(f.name).split('.')[0] + '.pdf'
    pdf_path = os.path.normpath(pdf_path)
    print('pdf',pdf_path)
    doc_path = '/media/' + str(f.name).split('.')[0] + '.pdf'

    if response:
        print('pdf generated')
        with open(pdf_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024*1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
                    os.fsync(f.fileno())
                    print('write')

    doc = Document(pdf_copy=doc_path, created_by=request.user.id)
    doc.save()

    async_task('invoice.views.autofill_async', doc.id)

    return redirect('home')


class Demo(TemplateView):
    template_name = 'trail.html'


class Testing(TemplateView):
    template_name = 'trail.html'


def api_call(request,pk):
    context = {}
    path_file = Document.objects.get(id=pk)
    pdf_file = str(path_file.pdf_copy).split('.')[0] + '.pdf'
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

    invoice_number = response['invoice_number']
    invoice_date = response['invoice_date']
    gstin = response['vendor_gstin']
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
        # form.fields['sgst'].initial = sgst[0]['value']
        pass
    if cgst:
        # form.fields['cgst'].initial = cgst[0]['value']
        pass
    if igst:
        # form.fields['igst'].initial = igst[0]['value']
        pass
    if total_taxable_amount:
        form.fields['total_taxable_amount'].initial = total_taxable_amount[0]['value']
    if vendor_address:
        form.fields['vendor_address'].initial = vendor_address[0]['value']

    path_file = Document.objects.get(id=pk)
    context['docs'] = path_file
    context['form'] = form

    return render(request,'invoice-create.html',context=context)


def logout(request):
    auth.logout(request)
    if not request.user.is_authenticated:
        print('Not logged in')
    return redirect('/auth/')

