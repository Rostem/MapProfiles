from django.contrib import admin

# Register your models here.
#from .models import Data, Machine, Date_meas, Energy, UploadConfig,
from .models import UploadData, UploadBaselines, Config, UploadCSV, PlotTrends

#admin.site.register(Data)
#admin.site.register(Energy)
#admin.site.register(Machine)
#admin.site.register(Date_meas)
#admin.site.register(UploadConfig)

admin.site.register(UploadData)
admin.site.register(UploadBaselines)
admin.site.register(Config)
admin.site.register(UploadCSV)
admin.site.register(PlotTrends)
