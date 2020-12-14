from django.db import models

# Create your models here.
class Data(models.Model):
	config_path = models.CharField(max_length=200, blank=True)
	default_config_path = models.CharField(max_length=200, default=None)
	machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, null=True)
	date_meas = models.ForeignKey('Date_meas', on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.pattern1 + '-' +  self.pattern2

class Machine(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name

class Date_meas(models.Model):
	name = models.CharField(max_length=100)

	class Meta:
		ordering = ['name']

	def __str__(self):
		return self.name	
