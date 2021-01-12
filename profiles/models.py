from django.db import models
import uuid # Required for unique scan instances

# Create your models here.
class Data(models.Model):
	data_path = models.CharField(max_length=200, default=None, null=True, blank=True)
	config_path = models.ForeignKey('ConfigPath', on_delete=models.SET_NULL, blank=True, null=True)
	machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, blank=True, null=True)
	date_meas = models.ForeignKey('Date_meas', on_delete=models.SET_NULL, blank=True, null=True)
	def __str__(self):
		return str(self.machine) + '-' +  str(self.date_meas)

class ConfigPath(models.Model):
	config_path = models.CharField(max_length=200)
	def __str__(self):
		return self.config_path

class Machine(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['-name']
	def __str__(self):
		return self.name

class Date_meas(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name

class Energy(models.Model):
	name = models.CharField(max_length=100)
	class Meta:
		ordering = ['name']
	def __str__(self):
		return self.name

# ======== file upload =============
#from django.contrib.auth.models import User
#def user_directory_path(instance, filename):
	#file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #return 'user_{0}/{1}'.format(instance.staff.id, filename)

class UploadConfig(models.Model):
	description = models.CharField(max_length=255, blank=True)
	#document = models.FileField(upload_to='documents/%Y/%m/%d/') - works
	config_file = models.FileField(upload_to='config')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	#document = models.FileField(upload_to=user_directory_path) - not working
	#staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

class UploadData(models.Model):
	data_files = models.FileField(upload_to='data')
	uploaded_at = models.DateTimeField(auto_now_add=True)


