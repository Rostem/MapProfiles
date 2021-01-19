import sys
import os
from io import StringIO

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.conf import settings

# needed for file downloads:
import pathlib
from django.http import FileResponse
from django.contrib import messages

from .src import prof
from .src import plots
from .src import conf
from profiles.models import UploadData, UploadBaselines, Config, UploadCSV, PlotTrends
from profiles.forms import UploadDataForm, UploadBaselinesForm, ConfigForm, UploadCSVForm, PlotTrendsForm
import csv

def show_manual(request):
	context = {
		'title': 'Manual',
		}
	return render(request, 'manual.html', context)

def show_about(request):
	context = {
		'title':  'About',
		'msg' : 'This app is written in Python 3.8 and uses Django 3.1 web development kit',
		}
	return render(request, 'message.html', context)

def show_contact(request):
	context = {
		'title':  'Contacts',
		'msg' : 'Please contact Rostem Bassalow for any questions.',
		}
	return render(request, 'message.html', context)

def reset_models():
	print('   views.reset_models: resetting all models')
	UploadData.objects.all().delete()
	UploadBaselines.objects.all().delete()
	Config.objects.all().delete()

@login_required
def index(request):
	reset_models()
	if request.method == 'POST':
		form = ConfigForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('upload-baselines') )
	else:
		form = ConfigForm()
	context = {
		'form': form,
		}
	return render(request, 'index.html', context)

def upload_baselines(request):
	if not os.path.isdir(settings.MEDIA_ROOT):
		os.mkdir(settings.MEDIA_ROOT)

	baselines_path = os.path.join(settings.MEDIA_ROOT, 'baselines')
	del_status = prof.delete_files(baselines_path)

	res_path = os.path.join(settings.MEDIA_ROOT, 'results')
	if os.path.isdir(res_path):
		del_status = prof.delete_files(res_path)
	else: os.mkdir(res_path)

	if request.method == 'POST':
		form = UploadBaselinesForm(request.POST, request.FILES)
		files = request.FILES.getlist('baseline_files')
		if form.is_valid():
			for f in files:
				file_instance = UploadBaselines(baseline_files = f)
				file_instance.save()
			return HttpResponseRedirect(reverse('upload-data') )
	else:
		form = UploadBaselinesForm()
	context = {
		'form': form,
		}
	return render(request, 'upload_baselines.html', context)

def upload_data(request):
	data_path = os.path.join(settings.MEDIA_ROOT, 'data')
	del_status = prof.delete_files(data_path)

	if request.method == 'POST':
		form = UploadDataForm(request.POST, request.FILES)
		files = request.FILES.getlist('data_files')
		if form.is_valid():
			for f in files:
				file_instance = UploadData(data_files = f)
				file_instance.save()
			return HttpResponseRedirect(reverse('analyze') )
	else:
		form = UploadDataForm()
	context = {
		'form': form,
		}
	return render(request, 'upload_data.html', context)

def analyze(request):
	config_model = get_object_or_404(Config)
	config = conf.GetConfig(config_model)

	data_path = os.path.join(settings.MEDIA_ROOT, 'data')
	baselines_path = os.path.join(settings.MEDIA_ROOT, 'baselines')
	res_path = os.path.join(settings.MEDIA_ROOT, 'results')

	data_files = os.listdir(data_path)
	baseline_files = os.listdir(baselines_path)
	machine, date_meas = prof.get_date_machine(data_files)
	_, baselines_date = prof.get_date_machine(baseline_files)
	print(f'   analyze: guessing {machine=}, {date_meas=}' )
	#context = {
		#'file_list': zip(data_files, baseline_files),
		#}
	#return render(request, 'analyze.html', context)

	data_dict = {
		'data_path': data_path,
		'baselines_path': baselines_path,
		'res_path': res_path,
		'machine': machine,
		'date_meas': date_meas,
		'baselines_date': baselines_date,
		}

	do, error_msg = prof.calc_profiles(data_dict, config)
	if error_msg:
		context = {
			'title': 'Error',
			'msg': error_msg,
			'msg': f'\n Please check that: all files follow strict naming convention. \
				\n Possible mismatch between the baselines and the monthly data. \
				\n Do the baselines and monthly share the same machine? \
				\n Do the baselines and monthly have the same spelling of the energies? '
			}
		return render( request, 'message.html', context=context )

	D, OAR_dif, FS_dif, oar_coord, data_fnames, base_fnames = do['D'], do['OAR_dif'], do['FS_dif'], do['oar_coord'], do['data_fnames'], do['base_fnames']

	# generates plot data:
	imgdata = StringIO()
	s_img =  machine + '-' + date_meas
	graph_oar = plots.return_oar_graph(imgdata, OAR_dif, oar_coord, res_path, s_img)

	imgdata = StringIO()
	graph_fs = plots.return_fs_graph(imgdata, FS_dif, res_path, s_img)

	imgdata = StringIO()
	graph_prof = plots.return_prof_graph(imgdata, D, res_path, s_img)
	imgdata.close()
	print( config.tol_oar_lo, config.tol_oar_hi)
	context = {
		'graph_oar': graph_oar,
		'graph_fs': graph_fs,
		'graph_prof': graph_prof,
		'tol_oar': {
			'p1': config.tol_oar_lo,
			'p2': config.tol_oar_hi,
			'n1': -config.tol_oar_lo,
			'n2': -config.tol_oar_hi,
			},
		'tol_fs' :{
			'p1': config.tol_fs_lo,
			'p2': config.tol_fs_hi,
			'n1': -config.tol_fs_lo,
			'n2': -config.tol_fs_hi,
			},
		'OAR_dif': OAR_dif,
		'FS_dif' : FS_dif,
		'oar_coord': oar_coord,
		'data_fnames': data_fnames,
		'base_fnames': base_fnames,
		'data_dict': data_dict,
		}
	return render(request, 'analyze.html', context)

def get_file_ext(path, ext):
	try:
		files = os.listdir(path)
	except:
		error_msg = f'  Could not find data to process. \n Data folder does not exit. \nWere the previous steps complete?'
		return None, error_msg

	f_ext = None
	if len(files) == 0:
		error_msg = '  Could not find data to process. \n Empty data folder. \nWere the previous steps complete?'
		return None, error_msg
	else:
		for f in files:
			if ext in f: f_ext = f
		if f_ext:
			return f_ext, None
		else:
			error_msg = f'   File(s) with {ext=} not found'
			return None, error_msg

def download_csv(request):
	res_path = os.path.join(settings.MEDIA_ROOT, 'results')
	res_files = os.listdir(res_path)
	sf, error_msg = get_file_ext(res_path, '.csv')
	if error_msg:
		context = {
			'title': 'Error',
			'msg': error_msg,
			}
		return render( request, 'message.html', context=context )

	file_path = os.path.join(settings.MEDIA_ROOT, 'results', sf)
	file_server = pathlib.Path(file_path)
	if not file_server.exists():
		messages.error(request, f'   results: {file_path=} not found.')
	else:
		file_to_download = open(str(file_server), 'rb')
		response = FileResponse(file_to_download, content_type = 'application/force-download')
		response['Content-Disposition'] = 'attachment; filename=' + sf
		return response
	return redirect('download_file.html')

def download_xls(request):
	res_path = os.path.join(settings.MEDIA_ROOT, 'results')
	res_files = os.listdir(res_path)
	sf, error_msg = get_file_ext(res_path, '.xls')
	if error_msg:
		context = {
			'title': 'Error',
			'msg': error_msg,
			}
		return render( request, 'message.html', context=context )

	file_path = os.path.join(settings.MEDIA_ROOT, 'results', sf)
	file_server = pathlib.Path(file_path)
	if not file_server.exists():
		messages.error(request, f'   results: {file_path=} not found.')
	else:
		file_to_download = open(str(file_server), 'rb')
		response = FileResponse(file_to_download, content_type = 'application/force-download')
		response['Content-Disposition'] = 'attachment; filename=' + sf
		return response
	return redirect('download_file.html')

def download_images(request):
	res_path = os.path.join(settings.MEDIA_ROOT, 'results')
	res_files = os.listdir(res_path)
	sf, error_msg = get_file_ext(res_path, '.png')
	if error_msg:
		context = {
			'title': 'Error',
			'msg': error_msg,
			}
		return render( request, 'message.html', context=context )

	file_path = os.path.join(settings.MEDIA_ROOT, 'results', sf)
	file_server = pathlib.Path(file_path)
	if not file_server.exists():
		messages.error(request, f'   results: {file_path=} not found.')
	else:
		file_to_download = open(str(file_server), 'rb')
		response = FileResponse(file_to_download, content_type = 'application/force-download')
		response['Content-Disposition'] = 'attachment; filename=' + sf
		return response
	return redirect('download_file.html')

#def results(request):
	#res_path = os.path.join(settings.MEDIA_ROOT, 'results')
	#res_files = os.listdir(res_path)
	#image_files =[]
	#for f in res_files:
		#if '.csv' in f: csv_file = os.path.join(settings.MEDIA_ROOT, 'results', f)
		#if '.xls' in f: xls_file = os.path.join(settings.MEDIA_ROOT, 'results', f)
		#if '.png' in f: image_files.append(os.path.join(settings.MEDIA_ROOT, 'results', f) )
	#print(f'   results: found {csv_file=}')
	#print(f'   results: found {xls_file=}')
	#print(f'   results: found {image_files=}')
	#links = {
		#'csv_file': csv_file,
		#'xls_file':  xls_file,
		#'image_files': image_files,
		#}
	#context = {
		#'title': 'Download Results',
		#'links': links,
		#}
	#return render( request, 'results.html', context=context )

def prepare_trends(request):
	UploadCSV.objects.all().delete()
	user_csv_path = os.path.join(settings.MEDIA_ROOT, 'user_csv')
	del_status = prof.delete_files(user_csv_path)

	if request.method == 'POST':
		form = UploadCSVForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('trends-form') )
	else:
		form = UploadCSVForm()
	context = {
		'form': form,
		}
	return render(request, 'prepare_trends.html', context)

def trends_form(request):
	PlotTrends.objects.all().delete()

	if request.method == 'POST':
		form = PlotTrendsForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('trends') )
	else:
		form = PlotTrendsForm()
	context = {
		'form': form,
		}
	return render(request, 'trends_form.html', context)

def trends(request):
	user_csv_path = os.path.join(settings.MEDIA_ROOT, 'user_csv', )
	csv_file, error_msg = get_file_ext(user_csv_path, '.csv')
	if error_msg:
		context = {
			'title': 'Error',
			'msg': error_msg,
			}
		return render( request, 'message.html', context=context )
	csv_path = os.path.join(user_csv_path, csv_file)

	config_model = get_object_or_404(Config)
	trends_model = get_object_or_404(PlotTrends)
	energy = trends_model.energy.upper().zfill(5)
	machine = csv_file[:-4]

	oar_x1, oar_x2, oar_x3, oar_x4 = [],[],[],[]
	oar_y1, oar_y2, oar_y3, oar_y4 = [],[],[],[]
	flat_x, flat_y = [],[]
	sym_x, sym_y = [],[]
	dates=[]
	#print (f'   trends: {csv_path=}, {energy=}, {machine=} ')

	with open(csv_path, newline='') as f_csv:
		reader = csv.DictReader(f_csv, dialect='excel')
		for row in reader:
			if  energy in str(row['energy']):
				dates.append( row['date'] )
				oar_x1.append( row['%dif OAR_X(-6.0)'])
				oar_x2.append( row['%dif OAR_X(-3.0)'])
				oar_x3.append( row['%dif OAR_X(3.0)'])
				oar_x4.append( row['%dif OAR_X(6.0)'])
				oar_y1.append( row['%dif OAR_Y(-6.0)'])
				oar_y2.append( row['%dif OAR_Y(-3.0)'])
				oar_y3.append( row['%dif OAR_Y(3.0)'])
				oar_y4.append( row['%dif OAR_Y(6.0)'])
				flat_x.append( row['Flat_X_dif'])
				flat_y.append( row['Flat_Y_dif'])
				sym_x.append( row['Sym_X_dif'])
				sym_y.append( row['Sym_Y_dif'])

	# generates plot data:
	s_img =  machine + '-' + energy
	eval_x = [config_model.eval_x1, config_model.eval_x2]

	imgdata = StringIO()
	oar_x= [oar_x1, oar_x2, oar_x3, oar_x4]
	trends_oar_x = plots.return_trends_oar(imgdata, dates, oar_x, user_csv_path, s_img, 'X ', 'OAR ', eval_x)

	imgdata = StringIO()
	oar_y= [oar_y1, oar_y2, oar_y3, oar_y4]
	trends_oar_y= plots.return_trends_oar(imgdata, dates, oar_y, user_csv_path, s_img, 'Y ', 'OAR ', eval_x)

	imgdata = StringIO()
	flat = [flat_x, flat_y]
	trends_flat= plots.return_trends_fs(imgdata, dates, flat, user_csv_path, s_img, 'Flatness')

	imgdata = StringIO()
	sym = [sym_x, sym_y]
	trends_sym = plots.return_trends_fs(imgdata, dates, sym, user_csv_path, s_img, 'Symmetry')

	imgdata.close()

	context = {
		'trends_oar_x': trends_oar_x,
		'trends_oar_y': trends_oar_y,
		'trends_flat': trends_flat,
		'trends_sym': trends_sym,
		'energy': energy,
		'machine': machine,
		}
	return render( request, 'trends.html', context=context )

# with open('path/test.pdf', 'rb') as pdf:
	# response = HttpResponse(pdf.read())
	# reponse['content_type'] = 'application/pdf'
	# response['Content-Disposition'] = 'attachment;filename=file.pdf'
	# return response