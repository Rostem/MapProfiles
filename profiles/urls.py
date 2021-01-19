from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('upload_baselines', views.upload_baselines, name='upload-baselines'),
	path('upload_data', views.upload_data, name='upload-data'),
	path('analyze', views.analyze, name='analyze'),
	path('download_csv', views.download_csv, name='download-csv'),
	path('download_xls', views.download_xls, name='download-xls'),
	path('download_images', views.download_images, name='download-images'),
	path('prepare_trends', views.prepare_trends, name='prepare-trends'),
	path('trends_form', views.trends_form, name='trends-form'),
	path('trends', views.trends, name='trends'),
	path('contact', views.show_contact, name='contact'),
	path('manual', views.show_manual, name='manual'),
	path('about', views.show_about, name='about'),
	#path('results/', views.results, name='results'),
]
