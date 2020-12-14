from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
	
from django.forms import ModelForm
from profiles.models import Data, Machine, Date_meas

#class EnterParamsForm(forms.Form):
	#config_path = forms.FilePathField(allow_files=False, allow_folders=True, path='/home/rb')
	#config_path = forms.CharField(label='Enter config_path', max_length=100)
	#pattern1 = forms.CharField(label='Enter machine name', max_length=100)
	#pattern2 = forms.CharField(label='Enter YYYY-MM', max_length=100)

class EnterParamsForm(ModelForm):
	class Meta:
		model = Data
		fields = [
			'config_path',
			'machine',
			'date_meas',
			]
		labels = {
			'config_path': _('Config path'),
			'machine': _('Machine'),
			'date_meas': _('Date of measurement'),
			}
		help_texts = {
			'config_path': _('Enter path to your config.dat'),
			'machine': _('Choose machine'),
			'date_meas': _('Choose date of measurement'),
			} 
