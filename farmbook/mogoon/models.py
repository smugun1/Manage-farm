from datetime import datetime

from django.db import models


# Create your models here.
class Employee(models.Model):
    national_identity = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=7)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    salary = models.IntegerField()

    def __str__(self):
        return self.name


class Crop(models.Model):
    plucking_date = models.DateTimeField(auto_now_add=False, blank=False)
    crop_data = models.CharField(max_length=50, default=False)
    crop_today = models.IntegerField()
    crop_todate = models.IntegerField(null=True, blank=True)
    plucker_numbers = models.IntegerField()
    total_pluckers = models.IntegerField(null=True, blank=True)
    plucking_average = models.IntegerField(null=True, blank=True)
    total_crop = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.crop_data)


class CropP(models.Model):
    plucking_date = models.DateTimeField(auto_now_add=False, blank=False)
    crop_data = models.CharField(max_length=50, default=False)
    crop_today = models.IntegerField()
    crop_todate = models.IntegerField(null=True, blank=True)
    plucker_numbers = models.IntegerField()
    total_pluckers = models.IntegerField(null=True, blank=True)
    plucking_average = models.IntegerField(null=True, blank=True)
    total_crops = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.crop_data)


class Kandojobs(models.Model):
    pruning_done = models.DateTimeField(auto_now_add=False)
    pruned_block_No = models.IntegerField()
    pruned_bushes = models.IntegerField()
    total_pruned_bushes = models.IntegerField(name=None, default=None)
    pruning_rate = models.DecimalField(max_digits=4, decimal_places=2, default=None)
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


class CashBreakdown(models.Model):
    cashBreakdown_date = models.DateTimeField(auto_now_add=False)
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    One_thousands = models.IntegerField(choices=list(zip(range(0, 100001), range(0, 100001))))
    Five_hundreds = models.IntegerField(choices=list(zip(range(0, 101), range(0, 101))))
    Two_hundreds = models.IntegerField(choices=list(zip(range(0, 101), range(0, 101))))
    One_hundreds = models.IntegerField(choices=list(zip(range(0, 101), range(0, 101))))
    Fifties = models.IntegerField(choices=list(zip(range(0, 101), range(0, 101))))
    Forties = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))
    Twenties = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))
    Tens = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))
    Fives = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))
    Ones = models.IntegerField(choices=list(zip(range(0, 11), range(0, 11))))

    def __str__(self):
        return str(self.cashBreakdown_date)


class Profile:
    pass
