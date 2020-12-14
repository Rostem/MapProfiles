from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required

from profiles.models import Data, Machine, Date_meas
from profiles.forms import EnterParamsForm
import sys
import os
from . import prof
from pathlib import Path

import matplotlib
matplotlib.use('Agg')  # to prevent getting Tk errors
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from io import StringIO
import numpy as np

class MachineListView(generic.ListView):    # is references in urls.py as path('scans/', views.ScanListView.as_view(),..)
	model = Machine   # will look for template in ../scans/templates/machine_list.html

class Date_measListView(generic.ListView):    # is references in urls.py as path('scans/', views.ScanListView.as_view(),..)
	model = Date_meas   # will look for template in ../scans/templates/machine_list.html

@login_required
def index(request):
	data = get_object_or_404(Data)
	if request.method == 'POST':
		form = EnterParamsForm(request.POST)
		if form.is_valid():
			print('index: data.config_path is currently = ', data.config_path )
			print('index: data.default.config_path is currently = ', data.default_config_path )
			if not data.config_path:
				data.config_path = form.cleaned_data['config_path']
			if not data.default_config_path: data.default_config_path = data.config_path  # change to user data QA folder on C
			data.machine = form.cleaned_data['machine']
			data.date_meas = form.cleaned_data['date_meas']
			data.save()
			return HttpResponseRedirect(reverse('plot-mpl') )

	# if a GET (or any other method) we'll create a blank form
	else:
		form = EnterParamsForm()

	context = {
		'form': form,
		'data': data,
		}

	return render(request, 'index.html', context)

class Config:
	def __init__(self, s_fin):
		fin = open(s_fin, 'r')
		lines = fin.readlines()
		for line in lines:
			if 'win_width' in line: self.win_width = int( line.split(',')[1].strip() )
			if 'win_height' in line: self.win_height = int( line.split(',')[1].strip() )
			if 'win_font_size' in line: self.font_size = line.split(',')[1].strip()
			if 'win_dpi' in line: self.dpi = int( line.split(',')[1].strip() )
			if 'win_marker_size' in line: self.marker_size = int( line.split(',')[1].strip() )
			if 'win_line_width' in line: self.line_w = int( line.split(',')[1].strip() )
			if 'detector_spacing' in line: self.det_spacing_cm = float( line.split(',')[1].strip() )
			if 'tolerance_mm' in line: self.tol_OAR= float( line.split(',')[1].strip() )
			if 'data_path' in line: self.data_path = line.split(',')[1].strip()
			if 'default_config_path' in line: self.default_config_path = line.split(',')[1].strip()
			if 'baseline_date' in line: self.baseline_date = line.split(',')[1].strip()
			if 'energy_list' in line: self.en_list = line.split(',')[1:]
			if 'field_size' in line: self.fs = float( line.split(',')[1].strip() )
			if 'eval_range' in line: self.eval_range = float( line.split(',')[1].strip() )
			if 'eval_coordinates' in line: self.X_eval = [ float(line.split(',')[1]), float(line.split(',')[2])  ]
		fin.close()
		self.calc_params()

	def calc_params(self):
		eval_dist_cm = self.eval_range * self.fs / 2  # cm
		self.n_eval = int(eval_dist_cm / self.det_spacing_cm)
		self.k_int = int ( self.det_spacing_cm/0.1)
		self.n_eval_sm = self.n_eval * self.k_int

def plot_style(i):
	s_color = ['r', 'b', 'g', 'c', 'm', 'y', 'k']
	s_marker = ['o', '+', 's', 'x', '^', '*' , '.' ]
	# s_line = ['solid', 'dashed', 'dashdot', 'dotted']
	s_line = ['--', '-.', ':', '-', '--', '-.'  , '-' ]
	if i<14:
		i%=7
		return s_color[i], s_marker[i], s_line[i]
	else:
		col = random.choice(s_color)
		mar = random.choice(s_marker)
		lin = random.choice(s_line)
		return col, mar, lin

def set_graphics(font_size):
	fig = plt.figure(figsize=(2, 2))
	#gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
	#axes = gs.subplots(sharex='col', sharey='row')
	fig, axes = plt.subplots(2, 1, sharex=False, sharey=False)
	#fig.suptitle('Profile analysis')

	s_ax = [
		'OAR X % dif',
		'OAR Y % dif',
		]
	for ax, s_ax in zip(axes, s_ax):
		ax.set_xlabel('cm', fontsize=font_size)
		ax.set_ylabel(s_ax, fontsize=font_size)
		ax.label_outer()
		ax.set_ylim(-1, 1)
		ax.tick_params(axis='both', labelsize=font_size)
		ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')
		#add_text_box(Ax[0][0], s_label)
	return axes, fig

def return_oar_graph(imgdata, OAR_X, OAR_Y, labels, s_img):
	font_size = 'medium'
	markersize = 5
	axes, fig = set_graphics(font_size)
	i_style = 0
	#axes[0].set_title('')
	for k, v in OAR_X.items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[0].plot(labels, v, color=s_color, marker=s_marker, linestyle=s_line, linewidth=1,  markersize=markersize, markevery=1, label=k)
		i_style +=1
	i_style = 0
	for k, v in OAR_Y.items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[1].plot(labels, v, color=s_color, marker=s_marker, linestyle=s_line, linewidth=1,  markersize=markersize, markevery=1, label=k)
		i_style +=1
	for axis in axes: axis.legend(loc='upper center', fancybox=True, shadow=True, framealpha=0.6, fontsize=font_size)

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	fig.savefig(s_img, format='png', transparent=False)
	del fig
	return  imgdata.getvalue()

def return_fs_graph(imgdata, FS, labels, s_img):
	font_size = 'medium'
	fig2 = plt.figure()
	fig2, ax = plt.subplots(1, 1, sharex=False, sharey=False)
	s_ax = '%'
	#ax.set_xlabel('cm', fontsize=font_size)
	ax.set_ylabel(s_ax, fontsize=font_size)
	ax.label_outer()
	ax.set_ylim(-3, 3)
	ax.tick_params(axis='both', labelsize=font_size)
	ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')
	#add_text_box(Ax[0][0], s_label)

	i_style = 0
	#axes[0].set_title('')
	for k, v in FS.items():
		s_color, s_marker, s_line = plot_style(i_style)
		style = s_color + s_marker
		ax.plot(labels, v, style, markersize=10, markevery=1, label = k)
		i_style +=1
	ax.legend(loc='upper center', fancybox=True, shadow=True, framealpha=0.6, fontsize=font_size)
	ax.plot(labels, [2,2,2,2], 'g-')
	ax.plot(labels, [-2,-2,-2,-2], 'g-')

	fig2.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	fig2.savefig(s_img, format='png', transparent=False)
	del fig2
	return  imgdata.getvalue()

def plot_mpl(request):
	data = get_object_or_404(Data)

	config_file = os.path.join(data.config_path, 'config.dat') if data.default_config_path else  os.path.join(data.default_config_path, 'config.dat')
	print('main: will look for config file:', config_file)
	if not os.path.isfile(config_file):
		print('main: ERROR: config file path not found:', config_file)
		got_data = False
		exit(0)
	else:
		print('main: SUCCESS: Config file found:', config_file)

	config = Config(config_file)
	data.default_config_path = config.default_config_path
	data.save()
	OAR_X, OAR_Y, FlatSym, s_coord, got_data = prof.calc_profiles(data, config)
	if not got_data:
		print ('main:  ERROR: data not found')
		context = {
			'error_msg': 'Data not found. Probably incorrect path(s) to data and/or baselines ...',
			}
		return render( request, 'error.html', context=context )

	imgdata = StringIO()
	oar_labels = s_coord
	s_img_oar = os.path.join( config.data_path, str(data.machine) + str(data.date_meas) + '_oar.png')
	graph_oar = return_oar_graph(imgdata, OAR_X, OAR_Y, oar_labels, s_img_oar)
	imgdata.close()

	imgdata2 = StringIO()
	fs_labels = [ 'flat_x', 'sym_x', 'flat_y', 'sym_y']
	s_img_fs = os.path.join( config.data_path, str(data.machine) + str(data.date_meas) + '_fs.png')
	graph_fs = return_fs_graph(imgdata2, FlatSym, fs_labels, s_img_fs)
	imgdata2.close()

	context = {
		'graph_oar': graph_oar,
		'graph_fs': graph_fs,
		'data': data,
		'config': config,
		'OAR_X': OAR_X,
		'OAR_Y': OAR_Y,
		'FlatSym' : FlatSym,
		}

	return render(request, 'plot_mpl.html', context)
