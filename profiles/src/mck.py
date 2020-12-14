import os
import numpy as np
from . import  data_filters as dfl
from . import prof_tools as ptl

class mapchk:
	def __init__(self, s_fin, config):
		fin = open(s_fin, 'r')
		self.s_f = os.path.split(s_fin)[1]
		self.lines = fin.readlines()
		self.got_data = False
		self.line_count = 0
		[self.line_before, self.nx, self.ny, self.ic, self.jc] = [0, 0, 0, 0, 0]
		fin.close()
		ksize_med = 3
		sigma_gauss = 1
		k_sg1, k_sg2 = 7, 3  # sav-gol parameters
		self.get_dose()     # -> self.x, self.dx
		self.xs, self.dxs = dfl.sg_filter(self.x, self.dx, config.k_int, k_sg1, k_sg2, config.n_eval+3)
		self.ys, self.dys = dfl.sg_filter(self.y, self.dy, config.k_int, k_sg1, k_sg2, config.n_eval+3)
		self.flat_x, self.sym_x, self.OAR_x = ptl.calc_prof_metrics(self.xs, self.dxs, config.X_eval, config.n_eval_sm)
		self.flat_y, self.sym_y, self.OAR_y = ptl.calc_prof_metrics(self.ys, self.dys, config.X_eval, config.n_eval_sm)
		self.sf =  self.s_f[:-4]
		self.get_map_pars(self.sf)
		
	def get_map_pars(self, s):
		a = s.split('-')
		self.machine,  self.date_meas, self.energy = a[0],  a[1]+'-'+a[2],  a[3]

	def get_dose(self):
		for line in self.lines:
			self.line_count += 1
			dat = line.split()
			# print (self.line_count, dat)
			if len(dat) > 0:
				if dat[0] == 'Rows:':
					self.ny = int(dat[1])
					self.y = np.zeros(self.ny, dtype=np.float32)
				if dat[0] == 'Cols:':
					self.nx = int(dat[1])
					self.x = np.zeros(self.nx, dtype=np.float16)
					self.D = np.zeros((self.ny, self.nx), dtype=np.float32)
				if dat[0] == 'CAX' and dat[1] == 'X:':
					self.ic = int(dat[2]) - 1
				if dat[0] == 'CAX' and dat[1] == 'Y:':
					self.jc = int(dat[2]) - 1
				if 'Dose Interpolated' in line: self.got_data = True
				if self.got_data and 'Ycm	ROW' in line:
					self.line_before = self.line_count
				if self.got_data and self.line_count > self.line_before and self.line_count < (self.line_before + self.ny + 1):
					j = self.line_count - self.line_before - 1
					self.y[j] = float(dat[0])
					for i in range(self.nx):
						self.x[i] = -(self.nx - 1) / 4 + i / 2
						self.D[j, i] = float(dat[i + 2])
		self.dx = self.D[self.jc, :]
		self.dy = self.D[:, self.ic]
		self.cax_val = self.D[self.jc, self.ic]
