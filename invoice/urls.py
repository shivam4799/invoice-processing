from django.urls import path
from .views import *

urlpatterns = [
    path('',InvoiceList.as_view(),name='home'),
    path('create',CreateForm.as_view(),name='create'),
    path('detail/<int:pk>',InvoiceDetailView.as_view(),name='detail'),
    path('delete/<int:pk>',InvoiceDeleteView.as_view(),name='delete'),
    path('update/<int:pk>',InvoiceUpdateView.as_view(),name='update'),
    path('billing',BillingPage.as_view(),name='billing'),
    path('setting',SettingsPage.as_view(),name='setting'),
    path('upload',upload,name='upload'),
    path('demo',Demo.as_view(),name='demo'),
    path('api',api_call,name='api'),
    path('logout',logout,name='logout')
]
