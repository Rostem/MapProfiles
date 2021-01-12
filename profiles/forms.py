from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm
from profiles.models import Data, Machine, Date_meas, Energy, ConfigPath

#config_path = forms.FilePathField(allow_files=False, allow_folders=True, path='/home/rb')

class EnterParamsForm(ModelForm):
	class Meta:
		model = Data
		fields = [
			'machine',
			'date_meas',
			]
		labels = {
			'machine': _('Machine'),
			'date_meas': _('Date of measurement'),
			}
		help_texts = {
			'machine': _('Choose machine'),
			'date_meas': _('Choose date of measurement'),
			}

class EnterConfigPathForm(ModelForm):
	class Meta:
		model = ConfigPath
		fields = [
			'config_path',
			]
		labels = {
			'config_path': _('config.dat full path'),
			}

# ======== file upload =============

from profiles.models import UploadConfig, UploadData
from django.forms import ClearableFileInput

class UploadConfigForm(ModelForm):
    class Meta:
        model = UploadConfig
        fields = ['config_file'	]

class UploadDataForm(ModelForm):
	class Meta:
		model = UploadData
		fields = ['data_files']
		widgets = {
			'data_files': ClearableFileInput(attrs={'multiple': True}),
			}
