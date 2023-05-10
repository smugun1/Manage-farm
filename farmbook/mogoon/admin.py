from django.contrib import admin
from .models import Green, Kandojobs, Fertilizer, Milk, Purple, Employee, Reports

# Register your models here.

admin.site.register(Employee)
admin.site.register(Green)
admin.site.register(Purple)
admin.site.register(Kandojobs)
admin.site.register(Fertilizer)
admin.site.register(Milk)
admin.site.register(Reports)



