from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Item)
admin.site.register(Invoice)
admin.site.register(Document)
admin.site.register(TagCoordinate)
