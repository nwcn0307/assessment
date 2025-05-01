import os
import sys
import json
from datetime import datetime
from django.core import management
from django.core.management.commands import loaddata, dumpdata
from django.apps import apps
from django.db import transaction
import tkinter as tk
from tkinter import filedialog


# =============== EXPORT DATA FUNCTIONS ===============

def export_data(app_label=None, model_name=None, output_file=None):
    """
    Export data from a specific model to a JSON file
    
    Args:
        app_label (str): The app label (e.g., 'activities')
        model_name (str): The model name (e.g., 'Activity')
        output_file (str): The output file name (default: app_label.json)
    
    Returns:
        str: Path to the exported file
    """
    if app_label is None or model_name is None:
        raise ValueError("Both 'app_label' and 'model_name' must be provided.")
# Prompt the user for app_label and model_name if not provided
        app_label = input("Enter the app label (e.g., 'products'): ").strip()
        model_name = input("Enter the model name (e.g., 'Product'): ").strip()

    if output_file is None:
#        output_file = f"DATABASE/JSON/{app_label}.json"
        output_file = f"DATABASE/JSON/{model_name.lower()}.json"
    
    try:
        # Use dumpdata command to export data
        management.call_command(
            'dumpdata', 
            f"{app_label}.{model_name}", 
            indent=4,
            output=output_file,
            natural_foreign=True,
            natural_primary=True
        )
        print(f"Data exported successfully to {output_file}")
        return output_file
    except Exception as e:
        print(f"Error exporting data: {str(e)}")
        return None

def export_all_data():
    """Export data from all models in all apps (excluding admin, auth, contenttypes, and sessions) to JSON files in a folder called 'Json'"""
    output_dir = "DATABASE/JSON"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    excluded_apps = {'admin', 'auth', 'contenttypes', 'sessions'}
    for app_config in apps.get_app_configs():
        app_label = app_config.label
        if app_label in excluded_apps:
            continue
        for model in app_config.get_models():
            model_name = model.__name__
            output_file = os.path.join(output_dir, f"{model_name.lower()}.json")
            export_data(app_label, model_name, output_file)
    print(f"All data exported successfully to the '{output_dir}' folder")

# =============== IMPORT DATA FUNCTIONS ===============

def import_data(input_file=None):
    """
    Import data from a JSON file into the database
    
    Args:
        input_file (str): The input file name (optional, will prompt user if not provided)
    
    Returns:
        bool: True if successful, False otherwise
    """
    input_dir = "DATABASE/JSON" # Default folder for JSON files
    if not os.path.exists(input_dir):
        print(f"Folder '{input_dir}' does not exist.")
        return False

    if input_file is None:
        root = tk.Tk()
        root.withdraw()  # Hide the root window

        input_file = filedialog.askopenfilename(
            initialdir=input_dir,
            title="Select a JSON file to import",
            filetypes=[("JSON files", "*.json")]
        )
        if not input_file:
            print("No file selected.")
            return False

    try:
        # Use loaddata command to import data
        management.call_command('loaddata', input_file)
        print(f"Data imported successfully from {input_file}")
        return True
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        return False

# def import_all_data():
#     """
#     Import data from all JSON files in the 'DATABASE/JSON' folder into the database.
#     Handles foreign key relationships by importing parent models first.
#     """
#     input_dir = "DATABASE/JSON"
#     if not os.path.exists(input_dir):
#         print(f"Folder '{input_dir}' does not exist.")
#         return False

#     # Get all JSON files in the directory
#     json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

#     # Sort files to ensure parent models are imported first
#     # You can customize the order based on your app's model dependencies
#     json_files.sort()

#     try:
#         for json_file in json_files:
#             input_file = os.path.join(input_dir, json_file)
#             print(f"Importing data from {input_file}...")
#             management.call_command('loaddata', input_file)
#         print(f"All data imported successfully from the '{input_dir}' folder.")
#         return True
#     except Exception as e:
#         print(f"Error importing data: {str(e)}")
#         return False
    
def import_all_data():
    """Import data from all JSON files in the 'Json' folder into the database"""
    input_dir = "DATABASE/JSON"
    if not os.path.exists(input_dir):
        print(f"Folder '{input_dir}' does not exist")
        return False
    
    for app_config in apps.get_app_configs():
        app_label = app_config.label
        for model in app_config.get_models():
            model_name = model.__name__
            input_file = os.path.join(input_dir, f"{model_name.lower()}.json")
            if os.path.exists(input_file):
                import_data(input_file)
    print(f"All data imported successfully from the '{input_dir}' folder")

# =============== GENERIC CRUD FUNCTIONS ===============

def clear_database():
    """Clear all data from the database except for excluded apps"""
    excluded_apps = {'admin', 'auth', 'contenttypes', 'sessions'}
    try:
        with transaction.atomic():
            # Delete all data from models in non-excluded apps
            for app_config in apps.get_app_configs():
                app_label = app_config.label
                if app_label in excluded_apps:
                    continue
                for model in app_config.get_models():
                    model.objects.all().delete()
            
            # Reset sequences for all models to avoid primary key conflicts
            for app_config in apps.get_app_configs():
                for model in app_config.get_models():
                    if hasattr(model, '_meta') and model._meta.managed:
                        management.call_command('sqlsequencereset', app_config.label, stdout=sys.stdout)
        
        print("Database cleared successfully (excluding excluded apps)")
        return True
    except Exception as e:
        print(f"Error clearing database: {str(e)}")
        return False

def clear_data(app_label):
    """Clear all data from the specified app in the database.

    Args:
        app_label (str): The label of the app to clear data from.
    """
    excluded_apps = {'admin', 'auth', 'contenttypes', 'sessions'}
    if app_label in excluded_apps:
        print(f"Cannot clear data for the excluded app: {app_label}")
        return False

    try:
        with transaction.atomic():
            # Get the app configuration
            app_config = apps.get_app_config(app_label)

            # Delete all data from models in non-excluded apps
            for model in app_config.get_models():
                model.objects.all().delete()
            
            # Reset sequences for all models to avoid primary key conflicts
            for model in app_config.get_models():
                if hasattr(model, '_meta') and model._meta.managed:
                    management.call_command('sqlsequencereset', app_label, stdout=sys.stdout)
        
        print(f"Database cleared successfully for the app: {app_label}")
        return True
    except LookupError:
        print(f"App '{app_label}' not found.")
        return False
    except Exception as e:
        print(f"Error clearing data for app '{app_label}': {str(e)}")
        return False



# =============== EXAMPLE USAGE ===============

def display_menu():
    """Display a list of commands for the user to choose from"""
    print("\n=== CRUD Operations Menu ===")
    print("1. Export all data")
    print("2. Import all data")
    print("3. Import data from a specific file")
    print("4. Clear all data")
    print("5. Exit")
    print("============================")

# def main():
#     """Main function to handle user input and execute commands"""
#     while True:
#         display_menu()
#         choice = input("Enter your choice (1-5): ").strip()
#         if choice == "1":
#             export_all_data()
#         elif choice == "2":
#             import_all_data()
#         elif choice == "3":
#             import_data()
#         elif choice == "4":
#             clear_database()
#         elif choice == "5":
#             print("Exiting...")
#             break
#         else:
#             print("Invalid choice. Please try again.")

#if __name__ == "__main__" or __name__ == "crud":
#    main()
