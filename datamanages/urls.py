from django.urls import path
from . import views

# Create your views here.

urlpatterns = [
    path('export-data/', views.export_data_view, name='export_data'),
    path('import-data/', views.import_data_view, name='import_data'),
    path('export-all-data/', views.export_all_data_view, name='export_all_data'),
    path('import-all-data/', views.import_all_data_view, name='import_all_data'),
    path('clear-data/', views.clear_data_view, name='clear_data'),
    path('clear-database/', views.clear_database_view, name='clear_database'),
    path('import_excel_data/', views.import_data_view, name='import_execl_data'),
    path('edit_st_data/<int:id>/', views.edit_st_data_view, name='edit_st_data'),  # Example edit view
    path('', views.datamanages, name='datamanages')

]