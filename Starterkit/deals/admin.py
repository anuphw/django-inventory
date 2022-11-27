from django.contrib import admin

# Register your models here.
from .models import Deal, Status, DealTimeline

admin.site.register(Deal)
admin.site.register(Status)
admin.site.register(DealTimeline)