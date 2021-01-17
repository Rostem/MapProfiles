class GetConfig:
	def __init__(self, config_model):
		self.fs = float(config_model.field_size)
		self.eval_range = float(config_model.eval_range)
		self.eval_x1 = float(config_model.eval_x1)
		self.eval_x2 = float(config_model.eval_x2)
		self.det_spacing_cm = 0.5
		self.tol_oar_lo = float(config_model.tol_oar_lo)
		self.tol_oar_hi = float(config_model.tol_oar_hi)
		self.tol_fs_lo = float(config_model.tol_fs_lo)
		self.tol_fs_hi = float(config_model.tol_fs_hi)
		self.flat_def =  config_model.flat_def
		self.sym_def =  config_model.sym_def
		self.calc_params()

	def calc_params(self):
		eval_dist_cm = self.eval_range * self.fs / 2  # cm
		self.n_eval = int(eval_dist_cm / self.det_spacing_cm)
		self.k_int = int ( self.det_spacing_cm/0.1)
		self.n_eval_sm = self.n_eval * self.k_int
