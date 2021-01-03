import os
import matplotlib
matplotlib.use('Agg')  # to prevent getting Tk errors
from matplotlib import pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
import random

def plot_style(i):
	s_color = ['r', 'b', 'g', 'c', 'm', 'y', 'k', 'pink',  'lime', 'gold', 'indigo' , '0.5',]
	s_marker = ['o', '+', 's', 'x', '^', '*' , '.', 'h', 'd', '>', 'p', '<' ]
	# s_line = ['solid', 'dashed', 'dashdot', 'dotted']
	s_line = ['-', '--', '-.', ':', '-', '--', '-.',  '-', '--', '-.', ':', '-' ]
	if i<24:
		i%=12
		return s_color[i], s_marker[i], s_line[i]
	else:
		col = random.choice(s_color)
		mar = random.choice(s_marker)
		lin = random.choice(s_line)
		return col, mar, lin

def normalize_cax(d):
	ic = len(d)//2
	d_cax = d[ic]
	return d/d_cax

def	return_prof_graph(imgdata, D, s_path, s_title):
	s_img = os.path.join(s_path, s_title)
	fig, axes = plt.subplots(2, 1, sharex=False, sharey=False, figsize=(6,4))  # set size of svg by figsize.
	font_size = 'x-small'
	markersize = 5
	y_labels = [
		'Dx/Dcax',
		'Dy/Dcax',
		]
	x_labels = [
		'X (cm)',
		'Y (cm)',
		]
	for ax, s_x, s_y in zip(axes, x_labels, y_labels):
		ax.set_xlabel(s_x, fontsize=font_size)
		ax.set_ylabel(s_y, fontsize=font_size)
		ax.label_outer()
		ax.tick_params(labelsize=font_size)
		ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')

	i_style = 0
	for  e, dat in D.items():
		s_color, s_marker, s_line = plot_style(i_style)
		dx = normalize_cax(dat['dx'])
		dy = normalize_cax(dat['dy'])
		axes[0].plot(dat['x'], dx, color=s_color, linestyle=s_line, linewidth=0.5,  label=e)
		axes[1].plot(dat['y'], dy, color=s_color, linestyle=s_line, linewidth=0.5,  label=e)
		i_style +=1

	for axis in axes:
		axis.set_title(s_title)
		axis.legend(loc='lower center', fancybox=True, shadow=True, framealpha=0.5, fontsize=font_size)
	plt.tight_layout()

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	#fig.savefig(s_img+'_xy_prof.png', format='png', transparent=False)
	del fig, axes
	return  imgdata.getvalue()

def return_oar_graph(imgdata, OAR_dif, oar_coord, s_path, s_title):
	s_img = os.path.join(s_path, s_title)
	font_size = 'medium'
	markersize = 5
	fig = plt.figure()
	fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(6,4))  # set size of svg by figsize.
	y_labels = [
		'OAR % Dif',
		'OAR % Dif',
		]
	x_labels = [
		'X (cm)',
		'Y (cm)',
		]

	for ax, s_x , s_y in zip(axes, x_labels, y_labels):
		ax.set_xlabel(s_x, fontsize=font_size)
		ax.set_ylabel(s_y, fontsize=font_size)
		#ax.label_outer()
		ax.set_ylim(-1.5, 1.5)
		#ax.tick_params(axis='both', labelsize=font_size)
		ax.tick_params(labelsize=font_size)
		ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')
		#add_text_box(Ax[0][0], s_label)

	i_style = 0
	for k, v in OAR_dif['X'].items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[0].plot(oar_coord, v, color=s_color, marker=s_marker, linestyle=s_line, linewidth=1, markersize=markersize, markevery=1, label=k)
		i_style +=1
	i_style = 0
	for k, v in OAR_dif['Y'].items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[1].plot(oar_coord, v, color=s_color, marker=s_marker, linestyle=s_line, linewidth=1, markersize=markersize, markevery=1, label=k)
		i_style +=1

	for axis in axes:
		axis.set_title(s_title)
		axis.legend(loc='upper center', fancybox=True, shadow=True, framealpha=0.5, fontsize=font_size)
	plt.tight_layout()

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	fig.savefig(s_img+'_oar.png', format='png', transparent=False)
	del fig, axes
	return  imgdata.getvalue()

def return_fs_graph(imgdata, FS,  s_path, s_title):
	s_img = os.path.join(s_path, s_title)
	font_size = 'medium'
	markersize = 5
	fig = plt.figure()
	fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(6,4))  # set size of svg by figsize.
	y_labels = [
		'F & S % dif',
		'F & S % dif',
		]
	x_labels = [
		'X (cm)',
		'Y (cm)',
		]
	s_coord = ['Flatness', 'Symmetry']

	for ax, s_x , s_y in zip(axes, x_labels, y_labels):
		ax.set_xlabel(s_x, fontsize=font_size)
		ax.set_ylabel(s_y, fontsize=font_size)
		ax.label_outer()
		ax.set_ylim(-1.5, 1.5)
		#ax.tick_params(axis='both', labelsize=font_size)
		ax.tick_params(labelsize=font_size)
		ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')

	i_style = 0
	for e, v in FS['X'].items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[0].scatter(s_coord, v, color=s_color, marker=s_marker, label = e)
		i_style +=1

	i_style = 0
	for e, v in FS['Y'].items():
		s_color, s_marker, s_line = plot_style(i_style)
		axes[1].scatter(s_coord, v, color=s_color, marker=s_marker, label = e)
		i_style +=1

	for axis in axes:
		axis.set_title(s_title)
		axis.legend(loc='upper center', fancybox=True, shadow=True, framealpha=0.5, fontsize=font_size)

	plt.tight_layout()
	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	#fig.savefig(s_img + '_fs.png', format='png', transparent=False)
	del fig, ax
	return  imgdata.getvalue()
