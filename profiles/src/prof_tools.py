import numpy as np

def coord_to_ind(x, xa):
	ia = np.argmin(abs(x-xa) )
	if type(ia) is list: print('   Warning: coord_to_ind found  >1 candidates ', ia)
	return ia

def calc_prof_metrics(u, du, X_eval, np_eval):
	"""
		Uses OAR calculations at 2 symmetric pairs of points (user can implement more) to sample a profile: 
		u  - coordinates of points
		du - doses at these points
	"""
	ic = len(u) // 2
	n3 = coord_to_ind(u, X_eval[0])
	n4 = coord_to_ind(u, X_eval[1])
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
	sym_aapm = round( (D_left.mean() - D_right.mean()) / (D_left.mean() + D_right.mean()) * 100 , 2)  # probably more robust, equivalent to integration
	# for i in range(np_eval):
	#	print(' {:>5.2f}  {:>5.2f}  {:>6.3f}  {:>6.3f}  {:>6.3f} '.format( X_left[i], X_right[i], D_left[i], D_right[i], D_left[i]-D_right[i] ) )

	dif = abs(D_left - D_right) # array of differences of symmetric points
	ind_max_dif = np.argmax(dif) # max dif here
	d_left_ind_max = D_left[ind_max_dif]  # dose value at the symmetric points of max dif
	d_right_ind_max = D_right[ind_max_dif]
	sym_max = round( 100 * 2 * (d_left_ind_max - d_right_ind_max) / (d_left_ind_max + d_right_ind_max) , 2)  # *2 to match Mapcheck Beam QA sym calc
	#sym_cax = round( (d_left_ind_max - d_right_ind_max) / d_cax * 100, 2)
	# print( 'indmax = {:3d},  dif={:>6.3f}  l={:>6.3f}  r={:>6.3f} '.format(ind_max_dif, dif[ind_max_dif], d_left_ind_max, d_right_ind_max) )

	d_eval_points = du[ic - np_eval: ic + np_eval + 1]   # use a central region for flatness
	flat = round( 100 * ( d_eval_points.max() - d_eval_points.min() ) / ( d_eval_points.max() + d_eval_points.min() ), 2)
	return flat, sym_aapm, OAR
