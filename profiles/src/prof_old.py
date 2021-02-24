#!/usr/bin/env python3
import numpy as np
import sys
import os
import glob
from matplotlib import pyplot as plt
import random
from .import data_filters as dfl
from .import mapcheck as MC
import pandas as pd

def get_date_machine(files):
	m_last, d_last = None, None
	#print(f'   get_date_machine: {files=}')
	for i, f in enumerate(files):
		if not '.txt' in f: break
		dat = f.split('-')
		m = dat[0]
		d = dat[1] + '-' + dat[2]
		if i>0:
			if m != m_last or d != d_last:
				print(f'   get_date_machine: {m=} ? {m_last=},    {d=} ? {d_last=}' )
			#else:
				#print(f'   get_date_machine: {m} = {m_last},    {d} = {d_last}' )
		m_last =m
		d_last = d
	return m, d

def delete_files(path):
	try:
		files = os.listdir(path)
		#print(f'   prof.delete_files: {files=}')
	except FileNotFoundError:
		print(f'   prof.delete_files: {path=} does not exist')
		return False
	except:
		print(f'   prof.delete_files: something wrong with {path=}')
		return False
	for f in files:
		f = os.path.join(path, f)
		os.remove(f)
	return True

def rename_files(path):
	try:
		files = os.listdir(path)
	except FileNotFoundError:
		print(f'   prof.rename_files: {path=} does not exist')
		return False
	except:
		print(f'   prof.rename_files: something wrong with {path=}')
		return False

	cnt_fi = 1
	for f in files:
		notxt = f.split('.')
		parts = notxt[0].split('-')
		np = len(parts)
		if np > 2:
			newname = ''
			for i in range(len(parts)):
				if i==3: parts[i] =  parts[i].upper().zfill(5)
				newname +=  (parts[i] + '-')  if i < (np-1)  else parts[i]
			newname += '.txt'
			if newname != f:
				for fi in files:
					if newname == fi:
						print(f'  prof.rename_files:  got double for: {fi}')
						newname= newname[:-4] + '-double' + str(cnt_fi) + '.txt'
						cnt_fi += 1
				oldf = os.path.join(path, f)
				newf = os.path.join(path, newname)
				os.rename(oldf, newf)
				print (f'   {f} -> {newname}')
			#else:
			#	print( f'     skipping: {f} = {newname}')
	return True

def find_matches(s_dir, s_pat):
	# s_fin = sorted(glob.glob( os.path.join(self._cwd, s_pat) ) )
	search_path = os.path.join(s_dir, s_pat)
	s_fin = sorted(glob.glob(search_path))
	return s_fin


def get_fieldnames(X_eval):
	pout = str(X_eval[1])
	pin = str(X_eval[0])
	nout = '-'+str(X_eval[1])
	nin =  '-'+str(X_eval[0])
	oar_coord = [nout, nin, pin, pout]
	col_names = ['machine', 'date', 'energy',
				'Flat_X', 'Sym_X', 'Flat_Y', 'Sym_Y',
				'OAR_X(' + nout + ')',
				'OAR_X(' + nin + ')',
				'OAR_X(' + pin + ')',
				'OAR_X(' + pout + ')',
				'OAR_Y(' + nout + ')',
				'OAR_Y(' + nin + ')',
				'OAR_Y(' + pin + ')',
				'OAR_Y(' + pout + ')',
				'Flat_X_dif', 'Sym_X_dif', 'Flat_Y_dif', 'Sym_Y_dif',
				'%dif OAR_X(' + nout + ')',
				'%dif OAR_X(' + nin + ')',
				'%dif OAR_X(' + pin + ')',
				'%dif OAR_X(' + pout + ')',
				'%dif OAR_Y(' + nout + ')',
				'%dif OAR_Y(' + nin + ')',
				'%dif OAR_Y(' + pin + ')',
				'%dif OAR_Y(' + pout + ')',
				]
	s_col_names = ','.join(col_names) + '\n'
	return 	s_col_names, oar_coord, col_names

def concat_data(s, A):
	s +=','.join(format(x, "5.3f") for x in A)
	return s

def get_s_metrics(M):
	s  =  M.machine + ',' +  M.date_meas + ',' + M.energy + ','
	s += str( round(M.flat_x,2) ) + ','
	s += str( round(M.sym_x,2) )+ ','
	s += str( round(M.flat_y,2) ) + ','
	s += str( round(M.sym_y,2) ) + ','
	s = concat_data(s, M.OAR_x) + ','
	s = concat_data(s, M.OAR_y) + ','
	return s

def check_add_s_metrics(X, tol, s):
	for x in X:
		if abs(x) > tol:
			print (f'  Tolerance = {tol: .1f} exceeded. Got {x:.2f}')
		s += str(x) + ','
	return s

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calc_profiles(data_dict, config):
	data_path = data_dict['data_path']
	baselines_path = data_dict['baselines_path']
	res_path = data_dict['res_path']
	s_machine = data_dict['machine']
	s_date = data_dict['date_meas']
	s_baselines_date = data_dict['baselines_date']
	s_data_match = '*' + s_machine + '*' + s_date + '*.txt'
	s_bl_match = '*' + s_machine + '*' + s_baselines_date + '*.txt'

	if not rename_files(data_path):
		error_msg = f'   calc_profiles: wrong data path'
		print(error_msg)
		return None, error_msg

	if not rename_files(baselines_path):
		error_msg = f'   calc_profiles: wrong baselines path'
		print(error_msg)
		return None, error_msg

	#print(f'   calc_profiles: Will look for files matching {s_machine} and {s_date} in {data_path} ' )
	s_data_files = find_matches(data_path, s_data_match)
	s_baseline_files = find_matches(baselines_path, s_bl_match)

	if not s_data_files or not s_baseline_files:
		error_msg = '   calc_profiles: data or baselines files were not found'
		print (error_msg)
		return None, error_msg
	else:
		print ('   calc_profiles: SUCCESS: files found')

	eval_x = [config.eval_x1, config.eval_x2]
	s_col_names, oar_coord, col_names = get_fieldnames(eval_x)
	csv_path = os.path.join(res_path, s_machine + '.csv')
	if os.path.isfile(csv_path):
		f_scv= open(csv_path,  'a' )
	else:
		f_scv= open(csv_path,  'w' )
		f_scv.write(s_col_names)

	xls_path = os.path.join(res_path, s_machine + '.xlsx')
	if os.path.isfile(xls_path):
		writer = pd.ExcelWriter(xls_path, mode='a', engine='openpyxl')
	else:
		writer = pd.ExcelWriter(xls_path, engine='openpyxl')
		#pd.set_option('max_colwidth', 400)

	D = {}
	OAR_dif = {
		'X':{},
		'Y':{},
		}
	FS = {
		'X':{},
		'Y':{},
		 }
	FS_dif = {
		'X':{},
		'Y':{},
		}
	data_fnames = {}
	base_fnames = {}

	i_row = 0
	for s_f in s_data_files:
		if not os.path.isfile(s_f):
			error_msg = f'   calc_profiles: could not find {s_f =}'
			print(error_msg)
			return None, error_msg
		else:
			Map = MC.Read_mpck(s_f, config)

		s_base_file = os.path.join(baselines_path, Map.machine + '-' + s_baselines_date  + '-' + Map.energy + '.txt')
		if not os.path.isfile(s_base_file):
			error_msg = f'   calc_profiles: could not find {s_base_file =}'
			print(error_msg)
			return None, error_msg
		else:
			Map_base = MC.Read_mpck(s_base_file, config)

		print('   {:20s}, baseline = {:20s}'.format(Map.sf, Map_base.sf) )
		data_fnames[Map.energy] = Map.sf
		base_fnames[Map.energy] = Map_base.sf

		D[Map.energy] = {
			'x': Map.xs,
			'dx': Map.dxs,
			'y': Map.ys,
			'dy': Map.dys,
			}

		FS['X'][Map.energy] = [Map.flat_x, Map.sym_x]
		FS['Y'][Map.energy] = [Map.flat_y, Map.sym_y]

		flat_dif_x = round(Map.flat_x -Map_base.flat_x,2)
		sym_dif_x = round(Map.sym_x - Map_base.sym_x,2)
		flat_dif_y = round(Map.flat_y -Map_base.flat_y,2)
		sym_dif_y = round(Map.sym_y - Map_base.sym_y,2)

		FS_dif['X'][Map.energy] = [flat_dif_x, sym_dif_x]
		FS_dif['Y'][Map.energy] = [flat_dif_y, sym_dif_y]

		s_metrics = get_s_metrics(Map)
		for x in FS_dif['X'][Map.energy]:
			s_metrics += str(x) + ','
		for x in FS_dif['Y'][Map.energy]:
			s_metrics += str(x) + ','

		OAR_dif_x = dfl.get_pct_dif (Map.OAR_x, Map_base.OAR_x)
		OAR_dif_y = dfl.get_pct_dif (Map.OAR_y, Map_base.OAR_y)
		OAR_dif['X'][Map.energy] = OAR_dif_x
		OAR_dif['Y'][Map.energy] = OAR_dif_y

		s_metrics = check_add_s_metrics(OAR_dif_x, config.tol_oar_lo, s_metrics)
		s_metrics = check_add_s_metrics(OAR_dif_y, config.tol_oar_lo, s_metrics)
		s_metrics += ' \n '
		f_scv.write(s_metrics)

		#print( f' OAR_dif_x,   OAR_dif_y =', OAR_X_dif[Map.energy], OAR_Y_dif[Map.energy] )
		#print( f' flat: x, y,  sym: x, y = { Map.flat_x: 5.2f}, { Map.flat_y: 5.2f}, { Map.flat_x: 5.2f}, { Map.flat_y: 5.2f}' )
		#print( f' flat_dif: x, y,  sym_dif: x, y = {flat_dif_x: 5.2f}, { flat_dif_y: 5.2f}, { sym_dif_x: 5.2f}, { sym_dif_y: 5.2f}' )

		if i_row == 0:
			df = pd.DataFrame(
				columns= col_names,
				)
			df.to_excel(writer, startrow = i_row, index = False, sheet_name= Map.date_meas)

			pd_data = [Map.machine, Map.date_meas, Map.energy, Map.flat_x , Map.sym_x, Map.flat_y, Map.sym_y] + Map.OAR_x + Map.OAR_y +  [flat_dif_x, sym_dif_x, flat_dif_y, sym_dif_y] + OAR_dif_x + OAR_dif_y

			df = pd.DataFrame(
				columns= pd_data,
				)
			df.to_excel(writer, startrow = i_row+1, index = False, sheet_name= Map.date_meas)
		else:
			pd_data = [Map.machine, Map.date_meas, Map.energy, Map.flat_x , Map.sym_x, Map.flat_y, Map.sym_y] + Map.OAR_x + Map.OAR_y +  [flat_dif_x, sym_dif_x, flat_dif_y, sym_dif_y] + OAR_dif_x + OAR_dif_y
			df = pd.DataFrame(
				columns= pd_data,
				)
			df.to_excel(writer, startrow = i_row+1, index = False, sheet_name= Map.date_meas)
		i_row +=1

	writer.save()
	writer.close()
	f_scv.close()
	del Map
	data_out = {
		'D': D,
		'OAR_dif': OAR_dif,
		'FS_dif': FS_dif,
		'oar_coord': oar_coord,
		'data_fnames': data_fnames,
		'base_fnames': base_fnames,
		}

	return  data_out, None
