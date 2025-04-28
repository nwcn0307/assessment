from django.contrib import admin, messages
from crud import export_all_data, import_all_data, clear_database, export_data, import_data
from django.contrib import admin
from .models import St_company, St_data

class CustomAdmin(admin.ModelAdmin):
    # Add custom actions
    actions = ['export_all_data_action', 'import_all_data_action', 'clear_database_action']
    def export_all_data_action(self, request, queryset):
        """Export all data to JSON files"""
        export_all_data()
        self.message_user(request, "All data exported successfully!", level=messages.SUCCESS)

    export_all_data_action.short_description = "Export All Data"

    def import_all_data_action(self, request, queryset):
        """Import all data from JSON files"""
        import_all_data()
        self.message_user(request, "All data imported successfully!", level=messages.SUCCESS)

    import_all_data_action.short_description = "Import All Data"

    def clear_database_action(self, request, queryset):
        """Clear all data from the database"""
        clear_database()
        self.message_user(request, "Database cleared successfully!", level=messages.WARNING)

    clear_database_action.short_description = "Clear Database"

# Add custom actions
    actions = ['export_data_action', 'import_data_action']


    def export_data_action(self, request, queryset):
        """Export data for the current model to a JSON file"""
        app_label = self.model._meta.app_label  # Get the app label dynamically
        model_name = self.model._meta.model_name  # Get the model name dynamically
        output_file = f"DATABASE/JSON/{model_name}.json"  # Define the output file path

        # Call the export_data function
        try:
            export_data(app_label, model_name, output_file)
            messages.success(request, f"Data exported successfully to {output_file}!")
        except Exception as e:
            messages.error(request, f"Error exporting data: {str(e)}")

    export_data_action.short_description = "Export Data"

    def import_data_action(self, request, queryset):
        """Import data for the current model from a JSON file"""
        app_label = self.model._meta.app_label  # Get the app label dynamically
        model_name = self.model._meta.model_name  # Get the model name dynamically
        input_file = f"DATABASE/JSON/{model_name}.json"  # Define the input file path

        # Call the import_data function
        try:
            success = import_data(input_file)
            if success:
                self.message_user(request, f"Data imported successfully from {input_file}!", level=messages.SUCCESS)
            else:
                self.message_user(request, f"Failed to import data from {input_file}.", level=messages.ERROR)
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

    import_data_action.short_description = "Import Data"


# Register your models here.
class St_dataAdmin(admin.ModelAdmin):
    list_display = ('code', 'date', 'price', 'qty')
    list_filter = ('code', 'date')
    search_fields = ('code', 'date')

admin.site.register(St_data, St_dataAdmin)

class St_companyAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    wearch_fields = ('code', 'name')

admin.site.register(St_company, St_companyAdmin)