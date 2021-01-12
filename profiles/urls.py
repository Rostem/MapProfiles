from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('params', views.params, name='params'),
	path('plot_mpl', views.plot_mpl, name='plot-mpl'),
	path('machines/', views.MachineListView.as_view(), name='machine-list'),
	path('date_meas/', views.Date_measListView.as_view(), name='date-meas-list'),
	path('success', views.plot_mpl, name='success'),
	path('contact', views.show_contact, name='contact'),
	path('manual', views.show_manual, name='manual'),
	path('about', views.show_about, name='about'),
	path('reset_data', views.reset_models, name='reset-data'),
]
