from .models import AppSettings
from datetime import datetime
def appsetting(request):
    settings,_ = AppSettings.objects.get_or_create()
    context = {
        'app_settings': settings,
        'date_today': datetime.today().strftime("%Y-%m-%d"),
    }
    return context