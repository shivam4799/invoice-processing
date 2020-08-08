from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import CreateView,ListView,TemplateView,DetailView,View
# Create your views here.
from .models import *
from .forms import *
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.db import transaction
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail


class CreateForm(CreateView):
    model = Invoice
    template_name = 'invoice-create.html'
    form_class = InvoicesForm

    def get_context_data(self, **kwargs):
        print('in get context data')
        data = super(CreateForm,self).get_context_data(**kwargs)
        path_file = Document.objects.filter().last()
        data['pdf_file'] = path_file.pdf_copy
        return data

    def form_valid(self, form):
        print('saving the form')
        self.object = form.save()
        # do something with self.object
        # remember the import: from django.http import HttpResponseRedirect
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('create')



class CreatePage(CreateView):
    model = Invoice
    template_name = 'invoice-preview.html'
    form_class = InvoiceForm

    def get_context_data(self, **kwargs):
        data = super(CreatePage, self).get_context_data(**kwargs)
        if self.request.POST:
            data['titles'] = ItemFormSet(self.request.POST)
            path_file = Document.objects.filter().last()
            data['pdf_file'] = path_file.pdf_copy
        else:
            data['titles'] = ItemFormSet()
            path_file = Document.objects.filter().last()
            data['pdf_file'] = path_file.pdf_copy
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        titles = context['titles']
        with transaction.atomic():
            #form.instance.created_by = self.request.user
            form.instance.created_by = 'demo123'
            self.object = form.save()
            if titles.is_valid():
                titles.instance = self.object
                titles.save()
        return super(CreatePage, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('create')


class InvoiceList(ListView):
    template_name = 'Dashboard.html'
    model = Invoice
    context_object_name = 'invoices'


class InvoiceDetailView(DetailView):
    model = Invoice
    template_name = 'invoice-detail.html'
    context_object_name = 'invoices_details'

    def get_context_data(self, **kwargs):
        context = super(InvoiceDetailView, self).get_context_data(**kwargs)
        return context


class BillingPage(TemplateView):
    template_name = 'billing.html'


class SettingsPage(TemplateView):
    template_name = 'settings_profile.html'


def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name,uploaded_file)
        url = fs.url(name)
        doc = Document(pdf_copy=url)
        doc.save()
        return redirect('/create')
    else:
        return redirect('/create')


def test(request):
    print('working fine')

    annotation_values = request.POST.get('annotation_values')
    invoice_id = request.POST.get('invoice_id')
    item_values = request.POST.get('item_values')
    # resp = request.POST.get('vals').split(':')[1].split(',')
    # label = request.POST.get('global_id_tag')
    # pageNum = request.POST.get('pageNum')
    # height = float(request.POST.get('height'))
    # width = float(request.POST.get('width'))
    # hmin = float(resp[0])/height
    # hmax = float(resp[1])/height
    # wmin = float(resp[2])/width
    # wmax = float(resp[3])/width
    # print(hmax,hmin,wmax,wmin)
    print('adding the values to model')

    print(annotation_values,invoice_id,item_values)
    # label_tag = TagCoordinate(label=label,hmin=hmin,hmax=hmax,wmin=wmin,wmax=wmax,page_id=pageNum)
    # label_tag.save()

    return JsonResponse({'status':200})


class Testing(TemplateView):
    template_name = 'testing.html'


def temp_data(request):
    item_d = request.POST.get('item_d')
    item_q = request.POST.get('item_q')
    item_r = request.POST.get('item_r')

    print('vals',item_d,item_q,item_r)

    temp = TempItem(item_q=item_q,item_r=item_r,item_d=item_d)
    temp.save()

    return HttpResponseRedirect('create')


class TempData(TemplateView):
    template_name = 'invoice-create.html'
