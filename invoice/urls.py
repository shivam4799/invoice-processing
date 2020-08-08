from django.urls import path
from .views import *

urlpatterns = [
    path('',InvoiceList.as_view(),name='home'),
    path('create',CreateForm.as_view(),name='create'),
    path('detail/<int:pk>',InvoiceDetailView.as_view(),name='detail'),
    path('billing',BillingPage.as_view(),name='billing'),
    path('setting',SettingsPage.as_view(),name='setting'),
    path('upload',upload,name='upload'),
    path('test',test,name='test'),
    path('additem',temp_data,name='additem'),
    path('testing',Testing.as_view(),name='testing'),
]
