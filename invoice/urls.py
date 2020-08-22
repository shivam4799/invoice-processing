from django.urls import path
from .views import *

urlpatterns = [
    path('',InvoiceListModel.as_view(),name='home'),
    path('invoices',InvoiceList.as_view(),name='invoices'),
    path('create/<int:pk>',CreateForm.as_view(),name='create_id'),
    # path('create', CreateForm.as_view(), name='create'),
    path('detail/<int:pk>',InvoiceDetailTemplate.as_view(),name='detail'),
    path('delete/<int:pk>',InvoiceDeleteView.as_view(),name='delete'),
    path('update/<int:pk>',InvoiceUpdateView.as_view(),name='update'),
    path('billing',BillingPage.as_view(),name='billing'),
    path('setting',SettingsPage.as_view(),name='setting'),
    path('bulkupload',BulkUploadView.as_view(),name='bulkupload'),
    path('upload',upload,name='upload'),
    path('demo',Demo.as_view(),name='demo'),
    path('api/<int:pk>',api_call,name='api'),
    path('logout',logout,name='logout'),
    path('upload_multiple',upload,name='upload_pdf'),
    path('upload_multiple_images',multipage_upload,name='upload_images'),
    path('fetch',fetch,name='fetch'),
    path('deletefetched/<int:id>',removeormakenull,name='removeormakenull')

]
