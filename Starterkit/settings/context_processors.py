from .models import AppSettings

def appsetting(request):
    settings,_ = AppSettings.objects.get_or_create()
    context = {
        'app_settings': settings,
    }
    return context