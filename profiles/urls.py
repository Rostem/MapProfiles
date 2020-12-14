from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('plot_mpl', views.plot_mpl, name='plot-mpl'),
	path('success', views.plot_mpl, name='success'),
	path('machines/', views.MachineListView.as_view(), name='machine-list'),
	path('date_meas/', views.Date_measListView.as_view(), name='date-meas-list'),
]
