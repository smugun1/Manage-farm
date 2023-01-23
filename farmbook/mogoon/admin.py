from django.contrib import admin
from .models import Crop, Kandojobs, Fertilizer, Milk, CropP, CashBreakdown, Employee

# Register your models here.

admin.site.register(Employee)
admin.site.register(Crop)
admin.site.register(CropP)
admin.site.register(Kandojobs)
admin.site.register(Fertilizer)
admin.site.register(Milk)
admin.site.register(CashBreakdown)


