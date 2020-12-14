#!/usr/bin/env python3
import numpy as np
import sys
import os
import glob
from matplotlib import pyplot as plt
import random
from .src import data_filters as dfl
from .src import mck
import pandas as pd

def find_matches(_dir, s_pat):
	# s_fin = sorted(glob.glob( os.path.join(self._cwd, s_pat) ) )
	s_fin = sorted(glob.glob(os.path.join(_dir, s_pat)))
	return s_fin


def get_fieldnames(X_eval):
	pout = str(X_eval[1])
	pin = str(X_eval[0])
	nout = '-'+str(X_eval[1])
	nin =  '-'+str(X_eval[0])
	s_coord = [nout, nin, pin, pout]
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
	return 	s_col_names, s_coord, col_names

def concat_data(s, A):
	s +=','.join(format(x, "5.3f") for x in A)
	return s

def get_s_metrics(M):
	s  =  M.machine + ',' +  M.date_meas + ',' + M.energy + ','
	s += str( M.flat_x ) + ','
	s += str( M.sym_x )+ ','
	s += str( M.flat_y ) + ','
	s += str( M.sym_y ) + ','
	s = concat_data(s, M.OAR_x)+ ','
	s = concat_data(s, M.OAR_y)+ ','
	return s

def check_add_s_metrics(X, tol, s):
	for x in X:
		if abs(x) > tol:
			print (f'  Tolerance of {tol: .1f} mm exceeded. Got {x:.2f}')
		s += str(x) + ','
	return s

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ MAIN ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def calc_profiles(data, config):
	got_data = True
	s_machine = str(data.machine)
	s_date = str(data.date_meas)
	s_match = '*' + s_machine + '*' + s_date + '*.txt'
	print('     Will look for files matching {} and {}'.format(s_machine, s_date))

	data_path = config.data_path
	print('     Will look for data files here:', data_path)

	s_files = find_matches(data_path, s_match)
	if not s_files:
		got_data = False
		print ('     ERROR: no data found')
		exit(0)
	else:
		print ('     Data files found:')

	s_col_names, s_coord, col_names = get_fieldnames(config.X_eval)
	s_prof = 'profile _const_' +  s_machine

	csv_path = os.path.join(data_path, s_prof + '.csv')
	if os.path.isfile(csv_path):
		f_scv= open(csv_path,  'a' )
	else:
		f_scv= open(csv_path,  'w' )
		f_scv.write(s_col_names)

	xls_path = os.path.join(data_path, s_prof + '.xlsx')
	if os.path.isfile(xls_path):
		writer = pd.ExcelWriter(xls_path, mode='a', engine='openpyxl')
	else:
		writer = pd.ExcelWriter(xls_path, engine='openpyxl')
		#pd.set_option('max_colwidth', 400)

	OAR_X = {}
	OAR_Y = {}
	FlatSym = {}

	if not s_files:
		print ('prof: ERROR: no data found')
		exit(0)

	i_row = 0
	for s_f in s_files:

		Map = mck.mapchk(s_f, config)
		print('\n {:20s} \n'.format(Map.sf) )
		s_base_file = os.path.join(data_path,  Map.machine + '-' + config.baseline_date + '-' + Map.energy + '.txt')
		Map_base = mck.mapchk(s_base_file, config)
		OAR_dif_x = dfl.get_pct_dif (Map.OAR_x, Map_base.OAR_x)
		OAR_dif_y = dfl.get_pct_dif (Map.OAR_y, Map_base.OAR_y)
		FlatSym[Map.energy]  = [Map.flat_x, Map.sym_x, Map.flat_y, Map.sym_y]

		s_metrics = get_s_metrics(Map)
		s_metrics = check_add_s_metrics(OAR_dif_x, config.tol_OAR, s_metrics)
		s_metrics = check_add_s_metrics(OAR_dif_y, config.tol_OAR, s_metrics)
		s_metrics += ' \n '
		f_scv.write(s_metrics)

		#if Map.energy.lower() in s_f.lower():
		OAR_X[Map.energy] = OAR_dif_x
		OAR_Y[Map.energy] = OAR_dif_y
		print( f' OAR_X dif  = ', OAR_X[Map.energy] )
		print( f' OAR_Y dif  = ', OAR_Y[Map.energy] )
		print( ' flat_x = {: 5.2f}'.format(Map.flat_x) )
		print( ' sym_x  = {: 5.2f}'.format(Map.sym_x) )
		print( ' flat_y = {: 5.2f}'.format(Map.flat_y) )
		print( ' sym_y  = {: 5.2f}'.format(Map.sym_y) )

		if i_row == 0:
			df = pd.DataFrame(
				columns= col_names,
				)
			df.to_excel(writer, startrow = i_row, index = False, sheet_name= Map.date_meas)

			pd_data = [Map.machine, Map.date_meas, Map.energy, Map.flat_x , Map.sym_x, Map.flat_y, Map.sym_y] + Map.OAR_x + Map.OAR_y + OAR_dif_x + OAR_dif_y
			df = pd.DataFrame(
				columns= pd_data,
				)
			df.to_excel(writer, startrow = i_row+1, index = False, sheet_name= Map.date_meas)
		else:
			pd_data = [Map.machine, Map.date_meas, Map.energy, Map.flat_x , Map.sym_x, Map.flat_y, Map.sym_y] + Map.OAR_x + Map.OAR_y + OAR_dif_x + OAR_dif_y
			df = pd.DataFrame(
				columns= pd_data,
				)
			df.to_excel(writer, startrow = i_row+1, index = False, sheet_name= Map.date_meas)
		i_row +=1

	writer.save()
	writer.close()
	f_scv.close()

	del Map
	data_out = OAR_X, OAR_Y, FlatSym, s_coord, got_data
	return data_out
