from django.contrib import admin
from .models import Green, Fertilizer, Milk, Purple, Employee, Reports, VetCosts, Pruning, Weeding

# Register your models here.

admin.site.register(Employee)
admin.site.register(Green)
admin.site.register(Purple)
admin.site.register(Pruning)
admin.site.register(Weeding)
admin.site.register(Fertilizer)
admin.site.register(Milk)
admin.site.register(VetCosts)
admin.site.register(Reports)



