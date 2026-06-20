from django.apps import AppConfig
import sys

class FuelapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.fuelApi'

    def ready(self):
        import sys
        is_running_server = 'runserver' in sys.argv or 'gunicorn' in sys.modules
        
        if is_running_server:
            from api.fuelApi.services.location_service import station_locator
            import threading
            
            def load_data():
                try:
                    station_locator.load_from_database()
                    print("Spatial tree successfully loaded in background!")
                except Exception as e:
                    print(f"Warning: Could not load spatial tree. Error: {e}")
            
            # Start the loading process in the background so Django doesn't complain
            threading.Thread(target=load_data, daemon=True).start()