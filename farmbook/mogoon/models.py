from datetime import datetime

from django.db import models


# Create your models here.
class Reports(models.Model):
    daily_report = models.CharField(max_length=250)
    visitors_name = models.CharField(max_length=100)
    visitor_comments = models.CharField(max_length=100)
    farm_report = models.CharField(max_length=100)
    farm_requirements = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.daily_report

    class Meta:
        ordering = ('-time_stamp',)


class Employee(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    DEPARTMENT_CHOICES = (
        ('Administration', 'Adm'), ('Security', 'Sec'), ('Management', 'Mgt'), ('Field', 'Fld'),
        ('Office', 'Off'), ('Stores', 'Str'), ('Other', 'Other'),
    )

    POSITION_CHOICES = (
        ('Guard', 'Grd'), ('Plucker', 'Plk'), ('Dairy', 'Dairy'), ('Kando', 'Kando'), ('Cook', 'Ck'),
        ('Office Messanger', 'Off Mgr'), ('Store', 'Str'), ('Director', 'Dir'), ('Estate Worker', 'Est Wkr'),
        ('Assistant Manager', 'Asst Mgr'), ('Accountant', 'Acct'), ('Supervisor', 'Sup'), ('Clerk', 'Clk'),
    )

    date_employed = models.DateTimeField(auto_now_add=False, blank=False)
    national_identity = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )
    department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, )
    position = models.CharField(max_length=100, choices=POSITION_CHOICES, )
    salary_total = models.IntegerField()

    def __str__(self):
        return self.name


class Green(models.Model):
    plucking_date = models.DateTimeField(auto_now_add=False, blank=False)
    green_data = models.CharField(max_length=50, default=False)
    green_today = models.IntegerField()
    green_todate = models.IntegerField(null=True, blank=True)
    plucker_numbers = models.IntegerField()
    total_pluckers = models.IntegerField(null=True, blank=True)
    plucking_average = models.IntegerField(null=True, blank=True)
    total_green = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.green_data)


class Purple(models.Model):
    plucking_date = models.DateTimeField(auto_now_add=False, blank=False)
    purple_data = models.CharField(max_length=50, default=False)
    purple_today = models.IntegerField()
    purple_todate = models.IntegerField(null=True, blank=True)
    plucker_numbers = models.IntegerField()
    total_pluckers = models.IntegerField(null=True, blank=True)
    plucking_average = models.IntegerField(null=True, blank=True)
    total_purple = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.purple_data)


class Kandojobs(models.Model):
    pruning_done = models.DateTimeField(auto_now_add=False)
    pruned_block_No = models.IntegerField()
    pruned_bushes = models.IntegerField()
    total_pruned_bushes = models.IntegerField(name=None, default=None)
    pruning_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)
    pruning_cost = models.DecimalField(max_digits=8, decimal_places=2)
    weeding_done = models.DateTimeField(auto_now_add=False, default=None)
    chemical_name = models.CharField(max_length=100, default=None)
    block_No = models.IntegerField(name=None, default=None)
    cost_per_lit = models.DecimalField(max_digits=8, decimal_places=2)
    weeding_chem_amt = models.DecimalField(max_digits=8, decimal_places=2)
    total_chem_amt = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    weeding_labour_number = models.IntegerField(name=None, default=None)
    total_weeding_labour_number = models.IntegerField(name=None, default=None)
    weeding_labour_rate = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    weeding_labour = models.IntegerField(name=None, default=None)
    weeding_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return str(self.pruned_bushes)


class Fertilizer(models.Model):
    fertilizer = models.CharField(max_length=20)
    fertilizer_applied = models.DateTimeField(auto_now_add=False)
    fertilizer_amt = models.IntegerField()
    fertilizer_labour_rate = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    fertilizer_labour = models.IntegerField()
    fertilizer_labour_cost = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    fertilizer_price = models.DecimalField(max_digits=8, decimal_places=2, default=None)
    fertilizer_cost = models.DecimalField(max_digits=8, decimal_places=2)
    fertilizer_total_cost = models.DecimalField(max_digits=8, decimal_places=2, default=None)

    def __str__(self):
        return str(self.fertilizer_amt)


class Milk(models.Model):
    milking_done = models.DateTimeField(auto_now_add=False)
    milk_today = models.DecimalField(max_digits=8, decimal_places=2)
    milk_todate = models.DecimalField(max_digits=8, decimal_places=2)
    cows_milked = models.IntegerField()
    cow_numbers = models.IntegerField()
    milking_average = models.DecimalField(max_digits=4, decimal_places=2)
    total_milk = models.DecimalField(max_digits=8, decimal_places=2)
    calf_down = models.DateTimeField(auto_now_add=True)
    today = models.DateTimeField(auto_now_add=False, blank=True, default=datetime.now())
    calf_age = models.IntegerField(name=None, default=None)
    calf_numbers = models.IntegerField(blank=True)
    vet_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    Total_vet_cost = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return str(self.milk_today)


class Profile:
    pass
