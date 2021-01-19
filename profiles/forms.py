from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from django.forms import ModelForm, ClearableFileInput

#from profiles.models import Data, Machine, Date_meas, Energy, UploadConfig
from profiles.models import Config, UploadData, UploadBaselines, UploadCSV, PlotTrends

#class AnalyzeForm(ModelForm):
	#class Meta:
		#model = Data
		#fields = [
			#'machine',
			#'date_meas',
			#]
		#labels = {
			#'machine': _('Machine'),
			#'date_meas': _('Date of measurement'),
			#}
		#help_texts = {
			#'machine': _('Choose machine'),
			#'date_meas': _('Choose date of measurement'),
			#}
#config_path = forms.FilePathField(allow_files=False, allow_folders=True, path='/home/rb')

class ConfigForm(ModelForm):
	class Meta:
		model = Config
		fields = '__all__'
		labels = {
			'eval_range': _('Evaluation range'),
			'eval_x1': _('first OAR distance'),
			'eval_x2': _('second OAR distance'),
			'tol_oar_lo': _('OAR % warning tolerance'),
			'tol_oar_hi': _('OAR % fail tolerance'),
			'tol_fs_lo': _('FS % warning tolerance'),
			'tol_fs_hi': _('FS % fail tolerance'),
			'flat_def': _('flatness defintion'),
			'sym_def': _('symmetry definition'),
			}

#class UploadConfigForm(ModelForm):
    #class Meta:
        #model = UploadConfig
        #fields = ['config_file'	]

class UploadBaselinesForm(ModelForm):
	class Meta:
		model = UploadBaselines
		fields = ['baseline_files']
		widgets = {
			'baseline_files': ClearableFileInput(attrs={'multiple': True}),
			}
		#help_texts={
			#'baseline_files': _('Press Load button after "No file chosen" changes to a number '),
			#}

class UploadDataForm(ModelForm):
	class Meta:
		model = UploadData
		fields = ['data_files']
		widgets = {
			'data_files': ClearableFileInput(attrs={'multiple': True}),
			}
		#help_texts={
			#'data_files': _('Press Load button after "No file chosen" changes to a number '),
			#}

class UploadCSVForm(ModelForm):
	class Meta:
		model = UploadCSV
		fields = [
			'user_csv_file',
			]

class PlotTrendsForm(ModelForm):
	class Meta:
		model = PlotTrends
		fields = [
			'energy',
			]
		help_texts={
			'energy': _('Energy must match one of those in your csv file'),
			}