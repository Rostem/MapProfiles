from django.contrib import admin

# Register your models here.
from .models import Data, Machine, Date_meas

admin.site.register(Data)
admin.site.register(Machine)
admin.site.register(Date_meas)
