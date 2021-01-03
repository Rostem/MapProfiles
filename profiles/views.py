from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from profiles.models import Data, Machine, Date_meas, Energy, ConfigPath
from profiles.forms import EnterParamsForm, EnterConfigPathForm
import sys
import os
from .src import prof
from .src import plots
from .src import config
from pathlib import Path

from io import StringIO
import numpy as np

class MachineListView(generic.ListView):    # is references in urls.py as path('scans/', views.ScanListView.as_view(),..)
	model = Machine   # will look for template in ../scans/templates/Machine_list.html

class Date_measListView(generic.ListView):    # is references in urls.py as path('scans/', views.ScanListView.as_view(),..)
	model = Date_meas   # will look for template in ../scans/templates/Machine_list.html

@login_required
def index(request):
	#cp = ConfigPath(config_path = ' ')
	ConfigPath.objects.all().delete()
	cp = ConfigPath()
	#cp = get_object_or_404(ConfigPath)
	print('   index: current path: ', cp.config_path )
	if request.method == 'POST':
		form = EnterConfigPathForm(request.POST)
		if form.is_valid():
			cp.config_path = form.cleaned_data['config_path']
			print('   index: current config path after save: ', cp.config_path )
			cp.save()
			return HttpResponseRedirect(reverse('params') )
	# if a GET (or any other method) we'll create a blank form
	else:
		form = EnterConfigPathForm()
	context = {
		'config_path': cp.config_path,
		'form': form,
		}
	return render(request, 'index.html', context)

def load_config():
	if (len(ConfigPath.objects.all() ) == 0):	return False, None
	cp = get_object_or_404(ConfigPath)
	print('   load_config: current path: ', cp.config_path )
	if not cp.config_path: 	return False, None
	config_file = os.path.join(cp.config_path, 'config.dat')
	print('   load_config: after joins got:', config_file)
	if not os.path.isfile(config_file):
		print('   load_config: config file not found:', config_file)
		return False, None
	else:
		print('   load_config: SUCCESS: Config file was found:', config_file)
		print('   load_config: will read config paramters now')
		return True, config.ReadConfig(config_file)

@login_required
def params(request):
	load_status, config = load_config()
	if not load_status:
		print ('   params:  config failed to load')
		context = {
			'title': 'Error',
			'msg': 'Config failed to load. \nPossibly wrong path or trying to Select Data \
					after Full Data Reset. \nPlease run Load Config first with the correct path to the config.dat file',
			}
		return render( request, 'message.html', context=context )
	fill_models(config)
	Data.objects.all().delete()
	data = Data()
	data.data_path = config.data_path
	print( f'   params: config.data_path: {config.data_path}' )

	if request.method == 'POST':
		form = EnterParamsForm(request.POST)
		if form.is_valid():
			if not data.data_path: 	print( '   params: WARNING: params: data.data_path = ', data.data_path)
			#data.data_path = config.data_path
			data.machine = form.cleaned_data['machine']
			data.date_meas = form.cleaned_data['date_meas']
			data.save()
			return HttpResponseRedirect(reverse('plot-mpl') )

	# if a GET (or any other method) we'll create a blank form
	else:
		form = EnterParamsForm()
	print( f'   params: data.data_path: {data.data_path}' )
	print( f'   params: data.machine: {data.machine}' )
	print( f'   params: data.date_meas: {data.date_meas}' )

	context = {
		'form': form,
		'data': data,
		}
	return render(request, 'params.html', context)

def show_manual(request):
	context = {
		'title': 'Manual',
		}
	return render(request, 'manual.html', context)

def show_about(request):
	context = {
		'title':  'About',
		'msg' : 'This app is written in Python 3 and uses Django (python) web development kit',
		}
	return render(request, 'message.html', context)

def show_contact(request):
	context = {
		'title':  'Contacts',
		'msg' : 'Please contact Rostem Bassalow for any questions.',
		}
	return render(request, 'message.html', context)

def reset_models(request):
	print('   views.reset_models: resetting all models')
	Date_meas.objects.all().delete()
	Machine.objects.all().delete()
	Energy.objects.all().delete()
	ConfigPath.objects.all().delete()
	Data.objects.all().delete()

	context = {
		'title': 'Warning',
		'msg':  'All cash has been cleared. \nPlease re-Load Config.',
		}
	return render(request, 'message.html', context)

def fill_models(config):
	all_machines = Machine.objects.all()
	all_dates = Date_meas.objects.all()
	all_Energies = Energy.objects.all()
	all_data = Data.objects.all()
	all_CP = ConfigPath.objects.all()

	print (f'\n   fill_models: before filling: \n')
	print (f'   fill_models: got {len(all_machines) } Machines, config has {len(config.machine_list)} machines' )
	print (f'   fill_models: got {len(all_Energies) } Energy, config has {len(config.energy_list)} energies' )
	print (f'   fill_models: got {len(all_dates) } Dates_meas, config has {len(config.date_list)} dates')
	print (f'   fill_models: got {len(all_data) } Data, should be 0')
	print (f'   fill_models: got {len(all_CP) } ConfigPath, should be 1')

	if ( len(all_machines)< len(config.machine_list) ):
		for m in config.machine_list:
			machine = Machine(name = m.strip())
			machine.save()
	if (len(all_dates)< len(config.date_list) ):
		for d in config.date_list:
			date_meas = Date_meas(name = d.strip())
			date_meas.save()
	if (len(all_Energies)< len(config.energy_list) ):
		for e in config.energy_list:
			en = Energy(name = e.strip())
			en.save()

	all_machines = Machine.objects.all()
	all_dates = Date_meas.objects.all()
	all_Energies = Energy.objects.all()

	print (f'   fill_models: after filling: \n')
	print (f'   fill_models: got {len(all_machines) } Machines, config has {len(config.machine_list)} machines' )
	print (f'   fill_models: got {len(all_Energies) } Energy, config has {len(config.energy_list)} energies' )
	print (f'   fill_models: got {len(all_dates) } Dates_meas, config has {len(config.date_list)} dates')

@login_required
def plot_mpl(request):
	load_status, config = load_config()
	if not load_status:
		print ('   plot_mpl:  config  failed to load')
		context = {
			'title': 'Error',
			'msg': 'Config path cannot be found. Please run Load Config first.',
			}
		return render( request, 'message.html', context=context )

	data = get_object_or_404(Data)
	data.data_path = config.data_path
	print (f'   plot_mpl:  { data.data_path = }')
	do, error_msg = prof.calc_profiles(data, config)
	if error_msg:
		context = {
			'title': 'Error',
			'error_msg': error_msg,
			'msg': f'\n\n Please check that: \
				\n- The following path contains both your baseline and monthly mapcheck files: { os.path.join(data.data_path, str(data.machine)) } \
				\n- and the baseline files only differs by the date from the monthly mapcheck file. \
				\n- Data folders match machine names exactly, \
				\n- Path to the config.dat file is correct, \
				\n- Naming of mapcheck files is of correct format.',
			}
		return render( request, 'message.html', context=context )

	D, OAR_dif, FS_dif, oar_coord, data_fnames, base_fnames = do['D'], do['OAR_dif'], do['FS_dif'], do['oar_coord'], do['data_fnames'], do['base_fnames']

	# generates plot data:
	if (str(data.machine).strip() !=0):
		imgdata = StringIO()
		s_img =  str(data.machine) + str(data.date_meas)
		graph_oar = plots.return_oar_graph(imgdata, OAR_dif, oar_coord, config.data_path, s_img)

		imgdata = StringIO()
		graph_fs = plots.return_fs_graph(imgdata, FS_dif, config.data_path, s_img)

		imgdata = StringIO()
		graph_prof = plots.return_prof_graph(imgdata, D, config.data_path, s_img)

		imgdata.close()

		context = {
			'graph_oar': graph_oar,
			'graph_fs': graph_fs,
			'graph_prof': graph_prof,
			'data': data,
			'config': config,
			'OAR_dif': OAR_dif,
			'FS_dif' : FS_dif,
			'oar_coord': oar_coord,
			'data_fnames': data_fnames,
			'base_fnames': base_fnames,
			}
		return render(request, 'plot_mpl.html', context)
	else:
		print ('   views.plot_mpl:  loading data from config... This is a necessary step."')
		context = {
			'title': 'Warning',
			'msg': 'loading data from config... This is a necessary step. \nSelect data again \
					- you should have all your Energies and machines imported now into the form choices',
			}
		return render( request, 'message.html', context=context )