class ReadConfig:
	def __init__(self, s_fin):
		fin = open(s_fin, 'r')
		lines = fin.readlines()
		for line in lines:
			if 'energy_list' in line: 
				self.energy_list = line.split(',')[1:]
				for m in self.energy_list: m = m.lower()
			if 'machine_list' in line: 
				self.machine_list = line.split(',')[1:]
				for m in self.machine_list: m = m.lower()
			if 'date_list' in line: self.date_list = line.split(',')[1:]
			if 'baseline_date' in line: self.baseline_date = line.split(',')[1].strip()
			if 'data_path' in line: self.data_path = line.split(',')[1].strip()
			if 'field_size' in line: self.fs = float( line.split(',')[1].strip() )
			if 'eval_range' in line: self.eval_range = float( line.split(',')[1].strip() )
			if 'eval_coordinates' in line: self.X_eval = [ float(line.split(',')[1]), float(line.split(',')[2])  ]
			if 'detector_spacing' in line: self.det_spacing_cm = float( line.split(',')[1].strip() )
			if 'tolerance_oar' in line:
				dat = line.split(',')[1:]
				tol =  [ float(v) for v in dat]
				self.tol_oar = { 'p1': tol[0], 'n1': -tol[0],
								'p2': tol[1], 'n2': -tol[1],
								}
			if 'tolerance_fs' in line:
				dat = line.split(',')[1:]
				tol =  [ float(v) for v in dat]
				self.tol_fs = { 'p1': tol[0], 'n1': -tol[0],
								'p2': tol[1], 'n2': -tol[1],
								}
			if 'flat_def' in line: self.flat_def =  line.split(',')[1].strip()
			if 'sym_def' in line: self.sym_def =  line.split(',')[1].strip()
			if 'win_width' in line: self.win_width = int( line.split(',')[1].strip() )
			if 'win_height' in line: self.win_height = int( line.split(',')[1].strip() )
			if 'win_font_size' in line: self.font_size = line.split(',')[1].strip()
			if 'win_dpi' in line: self.dpi = int( line.split(',')[1].strip() )
			if 'win_marker_size' in line: self.marker_size = int( line.split(',')[1].strip() )
			if 'win_line_width' in line: self.line_w = int( line.split(',')[1].strip() )
		fin.close()
		self.calc_params()

	def calc_params(self):
		eval_dist_cm = self.eval_range * self.fs / 2  # cm
		self.n_eval = int(eval_dist_cm / self.det_spacing_cm)
		self.k_int = int ( self.det_spacing_cm/0.1)
		self.n_eval_sm = self.n_eval * self.k_int
