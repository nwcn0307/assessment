from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from crud import export_all_data, import_all_data, clear_database, import_data, export_data
from excel_xlsx_csv import import_excel_data, data_to_django_fixture
from django.core.files.storage import FileSystemStorage
import pandas as pd
from .models import St_data, St_company
import os

def export_data_view(request):
    app_label = request.GET.get('app_label')  # Get app_label from the request
    model_name = request.GET.get('model_name')  # Get model_name from the request

    if not app_label or not model_name:
        messages.error(request, "Both 'app_label' and 'model_name' are required.")
        return redirect('/admin/')

    output_file = f"DATABASE/JSON/{model_name.lower()}.json"
    try:
        export_data(app_label, model_name, output_file)
        messages.success(request, f"Data exported successfully to {output_file}!")
    except Exception as e:
        messages.error(request, f"Error exporting data: {str(e)}")
    return redirect('/admin/')
    
def import_data_view(request):
        import_data()
        messages.success(request, "Data imported successfully!")
        return redirect('/admin/')
        
def export_all_data_view(request):
        export_all_data()
        messages.success(request, "All data exported successfully!")
        return redirect('/admin/')

def import_all_data_view(request):
        import_all_data()
        messages.success(request, "All data imported successfully!")
        return redirect('/admin/')

def clear_database_view(request):
        clear_database()
        messages.warning(request, "Database cleared successfully!")
        return redirect('/admin/')
# Create your views here.

# def import_execl_data_view(request):
#         import_execl_data()
#         messages.success(request, "Data imported successfully!")
#         return redirect('/admin/')
        
def datamanages(request):
    st_datas = None  # Initialize st_datas to None
    if request.method == 'POST' and request.FILES.get('excel_file'):
        # Handle file upload
        excel_file = request.FILES['excel_file']
        fs = FileSystemStorage()
        file_path = fs.save(excel_file.name, excel_file)
        file_path = fs.path(file_path)

        # Read the uploaded Excel file
        try:
            df = pd.read_excel(file_path, sheet_name='Sheet JS', header=0)
        except Exception as e:
            messages.error(request, f"Error reading Excel file: {str(e)}")
            return render(request, 'datamanages/datamanages.html', {"st_datas": st_datas})

        # Convert DataFrame to Django fixture format
        company = excel_file.name[2:6]
        if not St_company.objects.filter(code=company).exists():
            code=company
            name=excel_file.name
            St_company.objects.create(code=code,name=name)


        for _, row in df.iterrows():
            try:
            # Validate required fields
                if pd.isna(row['code']) or pd.isna(row['date']) or pd.isna(row['price']) or pd.isna(row['qty']):
                    messages.warning(request, f"Skipping row with missing data: {row}")
                    continue

                # Get or create the company
                company_instance, _ = St_company.objects.get_or_create(code=row['code'], defaults={'name': row.get('name', 'Unknown')})

                # Create and save the stock data
                St_data.objects.create(code=company_instance,  # Use the St_company instance
                date=row['date'],
                price=row['price'],
                qty=row['qty']
                )
            except Exception as e:
                print(f"Error: {e}")  # Debug: Print the error
                messages.error(request, f"Error saving data: {str(e)}")
                continue
            # for row in df.iterrows():
            #     if not st_datas:
            #         st_datas = St_data.objects.create(  code=company, date=row['date'], price=row['price'], qty=row['qty'])


        # Retrieve all data to display in the template
        st_datas = St_data.objects.all()
        #st_datas.save()
        messages.success(request, "Data imported and saved successfully!")
        # Ensure st_datas is not None
    if st_datas is None:
        st_datas = St_data.objects.all()

    context = {"st_datas" : st_datas}
    return render(request, 'datamanages/datamanages.html', context)

def edit_st_data_view(request, id):
      st_data = get_object_or_404(st_data, id=id)

      if request.method == 'post':
            #st_data.name = request.POST.get('name')
            st_data.date = request.POST.get('date')
            st_data.price = request.POST.get('price')
            st_data.Qty = request.POST.get('Qty')
            st_data.save()
            messages.success(request, "Data updated successfully!")
            return render(request, 'datamanages/edit_st_data.html', {'st_data': st_data})