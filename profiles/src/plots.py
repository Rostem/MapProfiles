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
		axis.legend(loc='lower right', fancybox=True, shadow=False, framealpha=0.5, fontsize='x-small')
	plt.tight_layout()

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	#fig.savefig(s_img+'_xy_prof.png', format='png', transparent=False)
	del fig, axes
	plt.close()
	return  imgdata.getvalue()

def return_oar_graph(imgdata, OAR_dif, oar_coord, s_path, s_title):
	s_img = os.path.join(s_path, s_title)
	font_size = 'medium'
	markersize = 5
	fig = plt.figure()
	fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(8,4))  # set size of svg by figsize.
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
		axis.legend(loc='upper center', fancybox=True, shadow=False, framealpha=0.5, fontsize=font_size)
	plt.tight_layout()

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	fig.savefig(s_img+'_oar.png', format='png', transparent=False)
	del fig, axes
	plt.close()
	return  imgdata.getvalue()

def return_fs_graph(imgdata, FS,  s_path, s_title):
	s_img = os.path.join(s_path, s_title)
	font_size = 'medium'
	markersize = 5
	fig = plt.figure()
	fig, axes = plt.subplots(1, 2, sharex=False, sharey=False, figsize=(8,4))  # set size of svg by figsize.
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
		axis.legend(loc='upper center', fancybox=True, shadow=False, framealpha=0.5, fontsize=font_size)

	plt.tight_layout()
	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)

	#fig.savefig(s_img + '_fs.png', format='png', transparent=False)
	del fig, ax
	plt.close()
	return  imgdata.getvalue()

def return_trends_oar(imgdata, s_coord, Y, s_path, s_title, s_lab, s_y, eval_coordinates):
	s_img = os.path.join(s_path, s_title)
	font_size = 'small'
	fig = plt.figure()
	fig, ax = plt.subplots(figsize=(8,4), tight_layout=True)  # set size of svg by figsize.
	y_label = s_y + s_lab + '% dif'
	ax.set_ylabel(y_label, fontsize=font_size)
	p1, p2 = eval_coordinates[0], eval_coordinates[1]
	labels = ['= -'+ str(p1) +' cm','= -'+ str(p2) +' cm','= '+ str(p1) +' cm','= '+ str(p2) +' cm']
	ax.set_ylim(-1.5,1.5)
	ax.set_yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], minor=False)
	ax.tick_params(axis='both', labelsize=font_size)

	for i in range(len(Y)):
		Y[i] = np.asarray(Y[i], dtype=np.float16)
		s_color, s_marker, s_line = plot_style(i)
		ax.plot(s_coord, Y[i], color=s_color, marker=s_marker, linestyle=s_line, linewidth=1, label = s_lab+' ' +labels[i])

	ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')
	ax.set_title(s_title)
	ax.legend(loc='upper center', fancybox=True, shadow=False, framealpha=0.5, fontsize=font_size)

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)
	#fig.savefig(s_img + '_fs.png', format='png', transparent=False)
	del fig, ax
	plt.close()
	return  imgdata.getvalue()

def return_trends_fs(imgdata, s_coord, Y, s_path, s_title, s_lab):
	s_img = os.path.join(s_path, s_title)
	font_size = 'small'
	fig = plt.figure()
	fig, ax = plt.subplots(figsize=(8,4), tight_layout=True)  # set size of svg by figsize.
	y_label = s_lab + ' % dif'
	ax.set_ylabel(y_label, fontsize=font_size)
	ax.set_ylim(-1.5,1.5)
	ax.set_yticks([-1.5, -1, -0.5, 0, 0.5, 1, 1.5], minor=False)
	ax.tick_params(axis='both', labelsize=font_size)
	labels = ['X', 'Y']

	for i in range(len(Y)):
		Y[i] = np.asarray(Y[i], dtype=np.float16)
		s_color, s_marker, s_line = plot_style(i)
		ax.plot(s_coord, Y[i], color=s_color, marker=s_marker, linestyle='-', linewidth=1, label = s_lab+' ' +labels[i])

	ax.grid(b=True, which='major', color='k', alpha=0.2, linewidth=0.5, linestyle='--')
	ax.set_title(s_title)
	ax.legend(loc='upper center', fancybox=True, shadow=False, framealpha=0.5, fontsize=font_size)

	fig.savefig(imgdata, format='svg', transparent=True)
	imgdata.seek(0)
	#fig.savefig(s_img + '_fs.png', format='png', transparent=False)
	del fig, ax
	plt.close()
	return  imgdata.getvalue()