import os
import sys
import pandas as pd
import json

from django.core import management
import tkinter as tk
from tkinter import filedialog
#from django.core.management.commands import loaddata, dumpdata

from crud import export_data, import_data

def import_excel_data(input_file=None):
    """
    Import data from a excel (xlsx) file into the database
    
    Args:
        input_file (str): The input file name (optional, will prompt user if not provided)
    
    Returns:
        bool: True if successful, False otherwise
    """
    input_dir = "DATABASE/xlsx" # Default folder for JSON files
    if input_file is None:
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        input_file = filedialog.askopenfilename(
            initialdir=input_dir,
            title="Select a excel(XLSX) file to import",
            filetypes=[("XLSX files", "*.xlsx")]
        )
        if not input_file:
            print("No file selected.")
            return False

    try:
        # Use loaddata command to import data
        df = pd.read_excel(file_path, sheet_name='Sheet JS', header=0, index_col=0)
        print(f"Data imported successfully from {input_file}")
        return True
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return False

def data_to_django_fixture(df):
    """
    Convert a DataFrame to Django JSON fixture format.
    """
    # Convert the DataFrame to a list of dictionaries
    data = df.reset_index().to_dict(orient='records')
    #print(data)
    # Prepare the data for Django JSON fixture format
    django_fixture = [
        {
            "model": "datamanges.st_data",
            #"model": "app_name.model_name",  # Replace with your app and model name
            "pk": index + 1,  # Primary key starts from 1
            "fields": record
        }
        for index, record in enumerate(data)
    ]
    return django_fixture

# Read the Excel fileexit
# file_path = '~/project/assessment/hk0001.xlsx'
# df = pd.read_excel(file_path, sheet_name='Sheet JS', header=0, index_col=0)

# #Convert the DataFrame to a list of dictionaries
# data = df.reset_index().to_dict(orient='records')
# print(data)
# # Prepare the data for Django JSON fixture format
# django_fixture = [
#     {
#         "model": "app_name.model_name",  # Replace with your app and model name
#         "pk": index + 1,  # Primary key starts from 1
#         "fields": record
#     }
#     for index, record in enumerate(data)
# ]
# #export_data(django_fixture)
# #print(django_fixture)

# def export_json_data(data, output_path='output.json'):
#     with open(output_path, 'w') as json_file:
#         json.dump(data, json_file, indent=4)
#     print(f"Data exported to {output_path}")

# # Save the fixture to a JSON file
# # output_path = '~/project/assessment/hk0001_fixture.json'
# # with open(output_path, 'w') as json_file:
# #     json.dump(django_fixture, json_file, indent=4)

# #print(f"Django JSON fixture saved to {output_path}")

# # Read the Excel file
# file_path = '~/project/assessment/hk0001.xlsx'
# df = pd.read_excel(file_path, sheet_name='Sheet JS', header=0, index_col=0)

# # Export the DataFrame to a CSV file
# output_csv_path = '~/project/assessment/hk0001_export.csv'
# df.to_csv(output_csv_path, index=True)  # Include the index in the CSV file

# print(f"Data exported to CSV file at {output_csv_path}")


# # Read the Excel file
# file_path = os.path.expanduser('~/project/assessment/hk0001.xlsx')
# df = pd.read_excel(file_path, sheet_name='Sheet JS', header=0, index_col=0)

# # Export the DataFrame to a CSV file
# output_csv_path = os.path.expanduser('~/project/assessment/hk0001_export.csv')
# df.to_csv(output_csv_path, index=True)  # Include the index in the CSV file

# print(f"Data exported to CSV file at {output_csv_path}")