import numpy as np
from scipy.interpolate import splev, splrep
from scipy.interpolate import interp1d
from scipy.ndimage import gaussian_filter
from scipy.signal import medfilt
from scipy.signal import savgol_filter

def _interp_splev(xlo, xhi, x, y, k_int):  # will generate xnew and ynew with n elements
	sp1 = splrep(x, y)
	n = (len(x) - 1) * k_int + 1
	x2 = np.linspace(xlo, xhi, n, dtype=np.float16)
	y2 = splev(x2, sp1)
	# ynew = spline(x, y, xnew, order=1, kind='smoothest', conds=None)   # smoothest
	return x2, y2

def _interp_1d(xlo, xhi, x, y, k_int):
	f = interp1d(x, y, kind='linear')  # quadratic , cubic - does not work
	n = (len(x) - 1) * k_int + 1
	x2 = np.linspace(xlo, xhi, n, dtype=np.float16)
	# x2 = np.around(x2, decimals=1)
	# print(x2)
	return x2, f(x2)

def gauss_filter(u, du, k_int, n_eval, sigma):
	ic = len(u) // 2
	dx = np.zeros(len(u), dtype=np.float32)
	dx[:ic - n_eval] = du[:ic - n_eval]
	dx[ic - n_eval:ic + n_eval + 1] =  gaussian_filter(du[ic - n_eval:ic + n_eval + 1], sigma, order=0, mode='reflect', cval=0.0, truncate=4.0)
	dx[ic + n_eval + 1:] = du[ic + n_eval + 1:]
	xs, dxs = _interp_1d(u[0], u[-1], u, dx, k_int)
	return xs, dxs

def med_filter( u, du, k_int, ksize_med):
	dx = medfilt(du, kernel_size=ksize_med)
	xs, dxs = _interp_1d(u[0], u[-1], u, dx, k_int)
	return xs, dxs

def sg_filter(u, du, k_int, k_sg1, k_sg2, n_eval):
	ic = len(u) // 2
	dx = np.zeros(len(u), dtype=np.float32)
	dx[:ic - n_eval] = du[:ic - n_eval]
	dx[ic - n_eval:ic + n_eval + 1] = savgol_filter(du[ic - n_eval:ic + n_eval + 1], k_sg1, k_sg2)
	dx[ic + n_eval + 1:] = du[ic + n_eval + 1:]
	#for i in range(len(u)): print('{:6.3f} {:6.3f} '.format(dx[i], du[i]) )
	xs, dxs = _interp_1d(u[0], u[-1], u, dx, k_int)
	return xs, dxs

def pct_dif (a, a_base, k_round):
	return round( (a-a_base)/a_base*100, k_round)

def get_pct_dif(X, X_base):
	s = []
	for x, x_base in zip(X, X_base): 	s.append( pct_dif( x, x_base, 2) )
	return s

