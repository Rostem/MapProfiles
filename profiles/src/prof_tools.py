import numpy as np

def val_to_ind(x, xa):
	ia = np.argmin(abs(x-xa) )
	if type(ia) is list: print('   Warning: val_to_ind found  >1 candidates ', ia)
	return ia

def calc_prof_metrics(u, du, config):
	"""
		Uses OAR calculations at 2 symmetric pairs of points (user can implement more) to sample a profile:
		u  - coordinates of points
		du - doses at these points
	"""
	X_eval, np_eval, flat_def, sym_def = config.X_eval, config.n_eval_sm, config.flat_def, config.sym_def

	ic = len(u) // 2
	n3 = val_to_ind(u, X_eval[0])
	n4 = val_to_ind(u, X_eval[1])
	n1 = len(u) - n4 - 1
	n2 = len(u) - n3 - 1
	d_cax = du[ic]
	lt1 = round( du[n1]/d_cax, 5)
	lt2 = round( du[n2]/d_cax, 5)
	rt1 = round( du[n3]/d_cax, 5)
	rt2 = round( du[n4]/d_cax, 5)
	OAR = [lt1, lt2, rt1, rt2]

	# uses smoothed data:
	ic = len(u) // 2
	d_cax = du[ic]
	X_left = u[ic - np_eval: ic]
	D_left = du[ic - np_eval: ic]
	X_right = np.flip( u[ic + 1: ic + np_eval + 1] )
	D_right = np.flip( du[ic + 1: ic + np_eval + 1] )
	LR_max = (D_left/D_right).max()
	RL_max = (D_right/D_left).max()
	# for i in range(np_eval):
	#	print(' {:>5.2f}  {:>5.2f}  {:>6.3f}  {:>6.3f}  {:>6.3f} '.format( X_left[i], X_right[i], D_left[i], D_right[i], D_left[i]-D_right[i] ) )

	dif = abs(D_left - D_right) # array of differences of symmetric points
	ind_max_dif = np.argmax(dif) # max dif here
	d_left_ind_maxdif = D_left[ind_max_dif]  # dose value at the symmetric points of max dif
	d_right_ind_maxdif = D_right[ind_max_dif]
	d_eval_points = du[ic - np_eval: ic + np_eval + 1]   # use a central region for flatness

	error_fs = False
	
	flat_maxmin = round( 100 * ( d_eval_points.max() - d_eval_points.min() ) / ( d_eval_points.max() + d_eval_points.min() ), 2)
	flat_IEC= round( 100 * (d_eval_points.max() /  d_eval_points.min()-1) , 2) # IEC 976 1989
	
	if 'iec' in flat_def.lower(): flat = flat_IEC 
	else:  flat = flat_maxmin
	
	sym_mean = round( 100 * (D_left.mean() - D_right.mean()) / (D_left.mean() + D_right.mean()) , 2) 
	sym_max = round( 100 * (d_left_ind_maxdif - d_right_ind_maxdif) / (d_left_ind_maxdif + d_right_ind_maxdif) , 2)
	sym_IEC = round( 100 * (max( [LR_max, RL_max] )-1) , 2)  #  IEC 9761989
	
	if 'max' in sym_def.lower(): sym = sym_max
	elif 'iec' in sym_def.lower(): sym = sym_IEC
	else: sym = sym_mean

	
	return flat, sym, OAR
