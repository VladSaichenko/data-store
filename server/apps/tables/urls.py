from django.urls import path

from . import views


urlpatterns = [
    path('', views.main_page, name='main_page'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('append_to_table/', views.append_to_csv, name='append_to_table'),
    path('add_column/', views.add_column, name='add_column')
]
