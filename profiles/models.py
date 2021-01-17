from django.db import models
import uuid # Required for unique scan instances
from django.contrib.auth.models import User

# Create your models here.
#class Data(models.Model):
	#data_path = models.CharField(max_length=200, default=None, null=True, blank=True)
	#baselines_path = models.CharField(max_length=200, default=None, null=True, blank=True)
	#config_path = models.CharField(max_length=200, default=None, null=True, blank=True)
	#machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, blank=True, null=True)
	#date_meas = models.ForeignKey('Date_meas', on_delete=models.SET_NULL, blank=True, null=True)
	#def __str__(self):
		#return str(self.machine) + '-' +  str(self.date_meas)

#class Machine(models.Model):
	#name = models.CharField(max_length=100)
	#class Meta:
		#ordering = ['-name']
	#def __str__(self):
		#return self.name

#class Date_meas(models.Model):
	#name = models.CharField(max_length=100)
	#class Meta:
		#ordering = ['name']
	#def __str__(self):
		#return self.name

#class Energy(models.Model):
	#name = models.CharField(max_length=100)
	#class Meta:
		#ordering = ['name']
	#def __str__(self):
		#return self.name

class Config(models.Model):
	field_size = models.IntegerField(default=20)
	eval_range= models.FloatField(default=0.8)
	eval_x1 = models.FloatField(default=3.0)
	eval_x2 = models.FloatField(default=6.0)
	tol_oar_lo = models.FloatField(default=1.0)
	tol_oar_hi  = models.FloatField(default=1.5)
	tol_fs_lo = models.FloatField(default=1.0)
	tol_fs_hi = models.FloatField(default=1.5)
	flat_choices = [
        ('maxmin', 'maxmin'),
        ('IEC', 'IEC'),
    ]
	flat_def = models.CharField(max_length=10, null=True, blank=True, choices = flat_choices, default='maxmin')
	sym_choices = [
        ('mean', 'mean'),
        ('max', 'max'),
        ('IEC', 'IEC'),
    ]
	sym_def  = models.CharField(max_length=10, null=True, blank=True, choices = sym_choices, default='mean')

#def user_directory_path(instance, filename):
	#file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.staff.id, filename)

#class UploadConfig(models.Model):
	#description = models.CharField(max_length=255, blank=True)
	#document = models.FileField(upload_to='documents/%Y/%m/%d/') - works
	#config_file = models.FileField(upload_to='config')
	#uploaded_at = models.DateTimeField(auto_now_add=True)
	#staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class UploadBaselines(models.Model):
	baseline_files = models.FileField(upload_to='baselines')
	uploaded_at = models.DateTimeField(auto_now_add=True)

class UploadData(models.Model):
	data_files = models.FileField(upload_to='data')
	uploaded_at = models.DateTimeField(auto_now_add=True)

class UploadCSV(models.Model):
	user_csv_file = models.FileField(upload_to='user_csv')
	plot_energy = models.CharField(max_length=5)
	uploaded_at = models.DateTimeField(auto_now_add=True)

class PlotTrends(models.Model):
	energy = models.CharField(max_length=5)

