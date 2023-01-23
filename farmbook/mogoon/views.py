import datetime
import pytz
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db.models import Sum, F, Count
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from . import models
from .forms import TaskForms, UpdateTaskForm, UpdateFertilizerForm, UpdateKandojobsForm, \
    UpdateMilkForm, UpdateCashBreakdownForm, CashBreakdownForm, EmployeeForm
from .models import *


# Create your views here.

@login_required(login_url='login')
@never_cache
def Home(request):
    context = {
        "name": {"Home Farm Page"},
        'form': TaskForms
    }
    return render(request, 'mogoon/home.html', context)


@never_cache
def Employee_details(request):
    if request.method == "POST":
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            national_identity = employee_form.cleaned_data['national_identity']
            name = employee_form.cleaned_data['name']
            age = employee_form.cleaned_data['age']
            gender = employee_form.cleaned_data['gender']
            department = employee_form.cleaned_data['department']
            position = employee_form.cleaned_data['position']
            salary = employee_form.cleaned_data['salary']

            employee = Employee(national_identity=national_identity, name=name, age=age, gender=gender,
                                department=department, position=position, salary=salary)
            employee.save()

            messages.success(request, 'Employee details are successfully saved.')
            return redirect('/employee-e_list')
    else:
        employee_form = EmployeeForm()
    return render(request, 'mogoon/employee_details.html', {'employee_form': employee_form})


def Employee_list(request):
    employee_list = Employee.objects.all()
    return render(request, 'mogoon/employee_list.html', {'employee_list': employee_list})


def Employee_update(request):
    employee_update = Employee.objects.all()
    return render(request, 'mogoon/employee_update.html', {'employee_update': employee_update})


# @login_required(login_url='login')
def Employee_edit(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee details are successfully updated.')
            return redirect('/employee-e_list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'Employee/update.html', {'form': form, 'employee': employee})


# @login_required(login_url='login')
def Employee_delete(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, 'Employee details are successfully deleted.')
        return redirect('/employee-e_details')
    context = {
        'item': employee,
    }
    return render(request, 'Employee/delete.html', context)


@never_cache
def CropTable(request):
    data = Crop.objects.all()
    plucking_date = models.DateTimeField()
    crop_today = Crop.objects.aggregate(all_count=Count('crop_today'))
    crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))
    plucker_numbers = Crop.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = Crop.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')
    total_crop = Crop.objects.aggregate(total_sum=Sum('crop_todate'))

    context = {
        "crop_data": data,
        "plucking_date": plucking_date,
        "c_today": crop_today,
        "c_todate": crop_todate,
        "p_numbers": plucker_numbers,
        "t_pluckers": total_pluckers,
        "p_average": plucking_average,
        "t_crop": total_crop,

    }
    return render(request, 'mogoon/crop_table.html', context)


# raise Exception("I want to know value" + str("Crop Table"))

@login_required(login_url='login')
@never_cache
def CropTableUpdate(request):
    crop_today = Crop.objects.count()
    # get the current crop_todate value
    crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))
    # the crop_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is nul as shown below, when null is set to type None and not type
    # Null
    if crop_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        crop_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the crop_todate and pass it to the templates via the context, this value
        # appears in the form
        crop_todate = Crop.objects.aggregate(all_sum=Sum('crop_today'))
    plucker_numbers = Crop.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = Crop.objects.aggregate(pl_total=Sum('plucker_numbers'))
    if total_pluckers.get('pl_total') is None:
        total_pluckers['pl_total'] = 0
    else:
        total_pluckers = Crop.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')
    if plucking_average is None:
        plucking_average = 0
    else:
        plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')

    total_crop = Crop.objects.aggregate(total_sum=Sum('crop_todate'))
    if total_crop.get('total_sum') is None:
        total_crop['total_sum'] = 0
    else:
        total_crop = Crop.objects.aggregate(total_sum=Sum('crop_todate'))

    context = {
        "crop_today": crop_today,
        "crop_todate": crop_todate,
        "plucker_numbers": plucker_numbers,
        "total_pluckers": total_pluckers,
        "plucking_average": plucking_average,
        "total_crop": total_crop,

    }
    return render(request, 'mogoon/crop_table_update.html', context)


@login_required(login_url='login')
@never_cache
def mogoonCropCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The crop_todate is the crop todate gotten from the
        # form(that was passed from the notes function) plus the crop today entered in the form.
        # Initially the crop to date is zero when the dta base is empty. the new crop to date will be zero plus the crop
        # today entered in the form, this addition is inserted and saved in the database as crop todate as shown below.
        plucking_date = request.POST['plucking_date']
        crop_data = request.POST['crop_data']
        crop_today = request.POST['crop_today']
        # Initially request.POST['crop_today'] is a string, it has to be wrapped with an int for purpose of addition
        crop_todate = int(request.POST['crop_todate']) + int(crop_today)
        plucker_numbers = request.POST['plucker_number']
        total_pluckers = request.POST['total_pluckers']
        plucking_average = request.POST['plucking_average']
        total_crop = request.POST['total_crop']

        insert = Crop(plucking_date=plucking_date, crop_data=crop_data, crop_today=crop_today, crop_todate=crop_todate,
                      plucker_numbers=plucker_numbers, total_pluckers=total_pluckers, plucking_average=plucking_average,
                      total_crop=total_crop)
        insert.save()

    return redirect('/crop_table')


@never_cache
def CropPurpleTable(request):
    data = CropP.objects.all()
    plucking_date = models.DateTimeField()
    crop_today = CropP.objects.count()
    crop_todate = CropP.objects.aggregate(all_sum=Sum('crop_today'))
    plucker_numbers = CropP.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = CropP.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')
    total_crop = CropP.objects.aggregate(total_sum=Sum('crop_todate'))

    context = {
        "crop_data": data,
        "plucking_date": plucking_date,
        "cs_today": crop_today,
        "cs_todate": crop_todate,
        "ps_numbers": plucker_numbers,
        "ts_total": total_pluckers,
        "ps_average": plucking_average,
        "t_crop": total_crop,

    }
    return render(request, 'mogoon/purple_tea.html', context)


# raise Exception("I want to know value" + str("Crop Table"))

@login_required(login_url='login')
@never_cache
def CropPurpleTableUpdate(request):
    # get the current crop_todate value
    crop_todate = CropP.objects.aggregate(all_sum=Sum('crop_today'))

    # the crop_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is nul as shown below, when null is set to type None and not type
    # Null
    if crop_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        crop_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the crop_todate and pass it to the templates via the context, this value
        # appears in the form
        crop_todate = CropP.objects.aggregate(all_sum=Sum('crop_today'))

    plucker_numbers = CropP.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = CropP.objects.aggregate(pl_total=Sum('plucker_numbers'))
    if total_pluckers.get('pl_total') is None:
        total_pluckers['pl_total'] = 0
    else:
        total_pluckers = CropP.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')
    if plucking_average is None:
        plucking_average = 0
    else:
        plucking_average = crop_todate.get('all_sum') // total_pluckers.get('pl_total')

    total_crop = CropP.objects.aggregate(total_sum=Sum('crop_todate'))
    if total_crop.get('total_sum') is None:
        total_crop['total_sum'] = 0
    else:
        total_crop = CropP.objects.aggregate(total_sum=Sum('crop_todate'))
    context = {
        "crop_todate": crop_todate,
        "plucker_numbers": total_pluckers,
        "total_pluckers": total_pluckers,
        "plucking_average": plucking_average,
        "total_crop": total_crop,

    }
    return render(request, 'mogoon/purple_tea_update.html', context)


@login_required(login_url='login')
@never_cache
def CropPurpleCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The crop_todate is the crop todate gotten from the
        # form(that was passed from the notes function) plus the crop today entered in the form.
        # Initially the crop to date is zero when the dta base is empty. the new crop to date will be zero plus the crop
        # today entered in the form, this addition is inserted and saved in the database as crop todate as shown below.
        plucking_date = request.POST['plucking_date']
        crop_data = request.POST['crop_data']
        crop_today = request.POST['crop_today']
        # Initially request.POST['crop_today'] is a string, it has to be wrapped with an int for purpose of addition
        crop_todate = int(request.POST['crop_todate']) + int(crop_today)
        plucker_numbers = request.POST['plucker_numbers']
        total_pluckers = request.POST.get('total_pluckers')
        plucking_average = request.POST['plucking_average']
        total_crop = request.POST['total_crop']

        insert = CropP(plucking_date=plucking_date, crop_data=crop_data, crop_today=crop_today,
                       crop_todate=crop_todate, plucker_numbers=plucker_numbers, total_pluckers=total_pluckers,
                       plucking_average=plucking_average, total_crop=total_crop)
        insert.save()

    return redirect('/purple_table')


@never_cache
def KandojobsTable(request):
    data = Kandojobs.objects.all()
    pruning_done = models.DateTimeField()
    pruned_block_No = models.IntegerField()
    pruned_bushes = Kandojobs.objects.aggregate(pr_count=Count('pruned_bushes'))
    total_pruned_bushes = Kandojobs.objects.aggregate(pr_sum=Sum('pruned_bushes'))
    pruning_rate = models.DecimalField()
    pruning_cost = pruned_bushes.get('pr_count') * F('pruning_rate')
    weeding_done = models.DateTimeField()
    chemical_name = models.CharField()
    block_No = models.IntegerField()
    cost_per_lit = models.DecimalField()
    weeding_chem_amt = Kandojobs.objects.aggregate(wc_amt=Count('weeding_chem_amt'))
    total_chem_amt = Kandojobs.objects.aggregate(tc_sum=Sum('weeding_chem_amt'))
    weeding_labour_number = Kandojobs.objects.aggregate(w_sum=Count('weeding_labour_number'))
    total_weeding_labour_number = Kandojobs.objects.aggregate(wl_sum=Sum('weeding_labour_number'))
    weeding_labour_rate = models.DecimalField()
    weeding_labour = weeding_labour_number.get('w_sum') * F('weeding_labour_rate')
    weeding_cost = (total_chem_amt.get('tc_sum') * F(cost_per_lit)) + weeding_labour

    context = {
        "kandojobs": data,
        "p_done": pruning_done,
        "p_b_No": pruned_block_No,
        "p_bushes": pruned_bushes,
        "tp_bushes": total_pruned_bushes,
        "p_rate": pruning_rate,
        "p_cost": pruning_cost,
        "w_done": weeding_done,
        "c_name": chemical_name,
        "b_No": block_No,
        "c_p_lit": cost_per_lit,
        "w_c_amt": weeding_chem_amt,
        "tc_amt": total_chem_amt,
        "wl_number": weeding_labour_number,
        "twl_number": total_weeding_labour_number,
        "wl_rate": weeding_labour_rate,
        "w_labour": weeding_labour,
        "w_cost": weeding_cost,
    }
    return render(request, 'mogoon/kandojobs_table.html', context)


@login_required(login_url='login')
@never_cache
def KandojobsTableUpdate(request):
    pruned_bushes = Kandojobs.objects.aggregate(pr_count=Count('pruned_bushes'))
    total_pruned_bushes = Kandojobs.objects.aggregate(pr_sum=Sum('pruned_bushes'))
    if total_pruned_bushes.get('pr_sum') is None:
        total_pruned_bushes['pr_sum'] = 0
    else:
        Kandojobs.objects.aggregate(pr_sum=Sum('pruned_bushes'))
    pruning_rate = models.DecimalField()
    pruning_cost = pruned_bushes.get('pr_count') * F('pruning_rate')
    if pruning_cost is None:
        pruning_cost = 0
    else:
        pruning_cost = pruned_bushes.get('pr_count') * F('pruning_rate')
    cost_per_lit = models.DecimalField()
    weeding_labour_number = Kandojobs.objects.aggregate(wl_num=Count('weeding_labour_number'))
    weeding_labour_rate = models.DecimalField()
    weeding_chem_amt = Kandojobs.objects.aggregate(wc_amt=Count('weeding_chem_amt'))
    total_chem_amt = Kandojobs.objects.aggregate(tc_sum=Sum('weeding_chem_amt'))
    if total_chem_amt.get('tc_sum') is None:
        total_chem_amt['tc_sum'] = 0
    else:
        total_chem_amt = Kandojobs.objects.aggregate(tc_sum=Sum('weeding_chem_amt'))
    total_weeding_labour_number = Kandojobs.objects.aggregate(wl_sum=Sum('weeding_labour_number'))
    if total_weeding_labour_number.get('wl_sum') is None:
        total_weeding_labour_number['wl_sum'] = 0
    else:
        total_weeding_labour_number = Kandojobs.objects.aggregate(wl_sum=Sum('weeding_labour_number'))
    weeding_labour = weeding_labour_number.get('w_sum') * F('weeding_labour_rate')
    if weeding_labour is None:
        weeding_labour = 0
    else:
        weeding_labour = weeding_labour_number.get('w_sum') * F('weeding_labour_rate')
    weeding_cost = (total_chem_amt.get('tc_sum') * F(cost_per_lit)) + weeding_labour
    if weeding_cost is None:
        weeding_cost = 0
    else:
        weeding_cost = (total_chem_amt.get('tc_sum') * F(cost_per_lit)) + weeding_labour

    context = {
        "pruned_bushes": pruned_bushes,
        "total_pruned_bushes": total_pruned_bushes,
        "pruning_rate": pruning_rate,
        "pruning_cost": pruning_cost,
        "weeding_labour_number": weeding_labour_number,
        "weeding_labour_rate": weeding_labour_rate,
        "weeding_chem_amt": weeding_chem_amt,
        "total_chem_amt": total_chem_amt,
        "weeding_labour": weeding_labour,
        "total_weeding_labour_number": total_weeding_labour_number,
        "weeding_cost": weeding_cost,

    }
    return render(request, 'mogoon/kandojobs_table_update.html', context)


@login_required(login_url='login')
@never_cache
def mogoonKandojobsCreate(request):
    if request.method == "POST":
        pruning_done = request.POST['pruning_done']
        pruned_block_No = request.POST['pruned_block_No']
        pruned_bushes = request.POST['pruned_bushes']
        total_pruned_bushes = request.POST['total_pruned_bushes']
        pruning_rate = request.POST['pruning_rate']
        pruning_cost = request.POST['pruning_cost']
        weeding_done = request.POST['weeding_done']
        chemical_name = request.POST['chemical_name']
        block_No = request.POST['block_No']
        cost_per_lit = request.POST['cost_per_lit']
        weeding_chem_amt = request.POST['weeding_chem_amt']
        total_chem_amt = request.POST['total_chem_amt']
        weeding_labour_number = request.POST['weeding_labour_number']
        total_weeding_labour_number = request.POST['total_weeding_labour_number']
        weeding_labour_rate = request.POST['weeding_labour_rate']
        weeding_labour = request.POST['weeding_labour']
        weeding_cost = request.POST['weeding_cost']

        insert = Kandojobs(pruned_block_No=pruned_block_No, pruned_bushes=pruned_bushes,
                           total_pruned_bushes=total_pruned_bushes, pruning_done=pruning_done,
                           pruning_rate=pruning_rate, pruning_cost=pruning_cost, weeding_done=weeding_done,
                           chemical_name=chemical_name, block_No=block_No, cost_per_lit=cost_per_lit,
                           weeding_chem_amt=weeding_chem_amt, total_chem_amt=total_chem_amt,
                           weeding_labour_number=weeding_labour_number, weeding_labour_rate=weeding_labour_rate,
                           weeding_labour=weeding_labour, total_weeding_labour_number=total_weeding_labour_number,
                           weeding_cost=weeding_cost)

        insert.save()
        return redirect('/kandojobs_table')


@never_cache
def MilkTable(request):
    data = Milk.objects.all()
    milking_done = models.DateTimeField()
    milk_today = Milk.objects.count()
    milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))
    cows_milked = Milk.objects.count()
    cow_numbers = Milk.objects.count()
    milking_average = F(milk_today) / F(cow_numbers)
    total_milk = Milk.objects.aggregate(total_sum=Sum('milk_todate'))
    calf_down = datetime.now(tz=pytz.UTC).replace(tzinfo=None)
    today = datetime.utcnow()
    calf_age = today - calf_down
    calf_numbers = Milk.objects.count()
    vet_cost = models.FloatField()
    Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))

    context = {
        "Milk": data,
        "m_done": milking_done,
        "m_today": milk_today,
        "m_todate": milk_todate,
        "c_milked": cows_milked,
        "c_numbers": cow_numbers,
        "m_average": milking_average,
        "t_milk": total_milk,
        "today": today,
        "cf_down": calf_down,
        "cf_age": calf_age,
        "cf_numbers": calf_numbers,
        "v_cost": vet_cost,
        "T_v_cost": Total_vet_cost,
    }
    return render(request, 'mogoon/milk_table.html', context)


@login_required(login_url='login')
@never_cache
def MilkTableUpdate(request):
    milk_today = Milk.objects.count()
    # get the current milk_todate value
    milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))

    # the milk_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is nul as shown below, when null is set to type None and not type
    # Null
    if milk_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        milk_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the milk_todate and pass it to the templates via the context, this value
        # appears in the form
        milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))
    cows_milked = Milk.objects.count()
    if cows_milked is None:
        cows_milked = 0
    else:
        Milk.objects.count()
    cow_numbers = Milk.objects.count()
    if cow_numbers is None:
        cow_numbers = 0
    else:
        Milk.objects.count()
    milking_average = F(milk_today) / F(cow_numbers)
    if milking_average is None:
        milking_average = milking_average
    else:
        milking_average = F(milk_today) / F(cow_numbers)
    total_milk = Milk.objects.aggregate(total_sum=Sum('milk_todate'))
    if total_milk.get('total_sum') is None:
        total_milk['total_sum'] = 0
    else:
        total_milk = Milk.objects.aggregate(total_sum=Sum('milk_todate'))
    calf_down = datetime.now(tz=pytz.UTC).replace(tzinfo=None)
    if calf_down is None:
        calf_down = 0
    else:
        calf_down = datetime.now(tz=pytz.UTC).replace(tzinfo=None)
    today = datetime.utcnow()
    calf_age = today - calf_down
    if calf_age is None:
        calf_age = 0
    else:
        calf_age = today - calf_down
    calf_numbers = Milk.objects.count()
    if calf_numbers is None:
        calf_numbers = 0
    else:
        Milk.objects.count()
    Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))
    if Total_vet_cost.get('total_cost') is None:
        Total_vet_cost['total_cost'] = 0
    else:
        Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))

    context = {
        "milk_todate": milk_todate,
        "cows_milked": cows_milked,
        "cow_numbers": cow_numbers,
        "milking_average": milking_average,
        "total_milk": total_milk,
        "calf_down": calf_down,
        "calf_age": calf_age,
        "calf_numbers": calf_numbers,
        "Total_vet_cost": Total_vet_cost,

    }
    return render(request, 'mogoon/milk_table_update.html', context)


@login_required(login_url='login')
@never_cache
def mogoonMilkCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The milk_todate is the Milk todate gotten from the
        # form(that was passed from the notes function) plus the Milk today entered in the form.
        # Initially the crop to date is zero when the dta base is empty. the new Milk to date will be zero plus the crop
        # today entered in the form, this addition is inserted and saved in the database as crop todate as shown below.
        milking_done = request.POST['milking_done']
        milk_today = request.POST['milk_today']
        milk_todate = int(request.POST['milk_todate']) + int(milk_today)
        # Initially request.POST['milk_today'] is a string, it has to be wrapped with an int for purpose of addition
        cows_milked = request.POST['cows_milked']
        cow_numbers = request.POST['cow_numbers']
        milking_average = request.POST['milking_average']
        total_milk = request.POST['total_milk']
        calf_down = request.POST['calf_down']
        calf_age = request.POST['calf_age']
        calf_numbers = request.POST['calf_numbers']
        vet_cost = request.POST['vet_cost']
        Total_vet_cost = request.POST['Total_vet_cost']

        insert = Milk(milking_done=milking_done, milk_today=milk_today, milk_todate=milk_todate,
                      cows_milked=cows_milked, cow_numbers=cow_numbers, milking_average=milking_average,
                      total_milk=total_milk, calf_down=calf_down, calf_age=calf_age, calf_numbers=calf_numbers,
                      vet_cost=vet_cost, Total_vet_cost=Total_vet_cost)
        insert.save()
        return redirect('/milk_table')


@never_cache
def FertilizerTable(request):
    data = Fertilizer.objects.all()
    fertilizer_applied = models.DateTimeField()
    fertilizer_amt = Fertilizer.objects.aggregate(ft_amt=Count('fertilizer_amt'))
    fertilizer_labour_rate = Fertilizer.objects.count()
    fertilizer_labour = Fertilizer.objects.aggregate(ft_lb=Count('fertilizer_labour'))
    fertilizer_labour_cost = F(fertilizer_amt) * F(fertilizer_labour_rate)
    fertilizer_price = models.IntegerField()
    fertilizer_cost = F(fertilizer_amt) * F(fertilizer_price)
    fertilizer_total_cost = fertilizer_cost + fertilizer_labour_cost

    context = {
        "fertilizer": data,
        "f_applied": fertilizer_applied,
        "f_amt": fertilizer_amt,
        "f_l_rate": fertilizer_labour_rate,
        "f_labour": fertilizer_labour,
        "f_l_cost": fertilizer_labour_cost,
        "f_price": fertilizer_price,
        "f_cost": fertilizer_cost,
        "f_t_cost": fertilizer_total_cost,

    }
    return render(request, 'mogoon/fertilizer_table.html', context)


@login_required(login_url='login')
@never_cache
def mogoonFertilizerTableUpdate(request):
    fertilizer_amt = Fertilizer.objects.count()
    fertilizer_labour_rate = models.DecimalField()
    fertilizer_labour = models.IntegerField()
    fertilizer_labour_cost = F(fertilizer_amt) * F(fertilizer_labour_rate)
    if fertilizer_labour_cost is None:
        fertilizer_labour_cost = 0
    else:
        fertilizer_labour_cost = F(fertilizer_amt) * F(fertilizer_labour_rate)
    fertilizer_price = models.DecimalField()
    fertilizer_cost = F(fertilizer_amt) * F(fertilizer_price)
    if fertilizer_cost is None:
        fertilizer_cost = 0
    else:
        fertilizer_cost = F(fertilizer_amt) * F(fertilizer_price)
    fertilizer_total_cost = fertilizer_cost + fertilizer_labour_cost
    if fertilizer_total_cost is None:
        fertilizer_total_cost = 0
    else:
        fertilizer_total_cost = fertilizer_cost + fertilizer_labour_cost
    context = {
        "fertilizer_amt": fertilizer_amt,
        "fertilizer_labour_rate": fertilizer_labour_rate,
        "fertilizer_labour": fertilizer_labour,
        "fertilizer_price": fertilizer_price,
        "fertilizer_labour_cost": fertilizer_labour_cost,
        "fertilizer_cost": fertilizer_cost,
        "fertilizer_total_cost": fertilizer_total_cost,

    }
    return render(request, 'mogoon/fertilizer_table_update.html', context)


@login_required(login_url='login')
@never_cache
def mogoonFertilizerCreate(request):
    if request.method == "POST":
        fertilizer = request.POST['fertilizer']
        fertilizer_applied = request.POST['fertilizer_applied']
        fertilizer_labour_rate = request.POST['fertilizer_labour_rate']
        fertilizer_amt = request.POST['fertilizer_amt']
        fertilizer_labour = request.POST['fertilizer_labour']
        fertilizer_labour_cost = request.POST['fertilizer_labour_cost']
        fertilizer_price = request.POST['fertilizer_price']
        fertilizer_cost = request.POST['fertilizer_cost']
        fertilizer_total_cost = request.POST['fertilizer_total_cost']

        insert = Fertilizer(fertilizer=fertilizer, fertilizer_applied=fertilizer_applied, fertilizer_amt=fertilizer_amt,
                            fertilizer_labour_rate=fertilizer_labour_rate,
                            fertilizer_labour=fertilizer_labour, fertilizer_labour_cost=fertilizer_labour_cost,
                            fertilizer_price=fertilizer_price,
                            fertilizer_cost=fertilizer_cost, fertilizer_total_cost=fertilizer_total_cost)
        insert.save()
        return redirect('/fertilizer_table')


@never_cache
def CashBreakdownTable(request):
    # calculate the change from each denomination
    note = CashBreakdown.objects.all()
    cashBreakdown_date = models.DateTimeField()
    amount = CashBreakdown.objects.aggregate(Sum('amount'))
    One_thousands = 0
    Five_hundreds = 0
    Two_hundreds = 0
    One_hundreds = 0
    Fifties = 0
    Forties = 0
    Twenties = 0
    Tens = 0
    Fives = 0
    Ones = 0
    if amount['amount__sum'] is not None:
        One_thousands = amount['amount__sum'] // 1000
        Five_hundreds = amount['amount__sum'] // 1000 // 500
        Two_hundreds = amount['amount__sum'] // 1000 // 500 // 200
        One_hundreds = amount['amount__sum'] // 1000 // 500 // 200 // 100
        Fifties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50
        Forties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40
        Twenties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20
        Tens = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10
        Fives = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5
        Ones = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5 // 1

    context = {
        "cashBreakdown": note,
        "cashBreakdown_date": cashBreakdown_date,
        "amount": amount,
        "One_thousands": One_thousands,
        "Five_hundreds": Five_hundreds,
        "Two_hundreds": Two_hundreds,
        "One_hundreds": One_hundreds,
        "Fifties": Fifties,
        "Forties": Forties,
        "Twenties": Twenties,
        "Tens": Tens,
        "Fives": Fives,
        "Ones": Ones,

    }
    return render(request, 'mogoon/cashBreakdown_table.html', context)


def CashBreakdownUpdate(request):
    amount = CashBreakdown.objects.aggregate(Sum('amount'))
    if not amount:
        amount = 0
    else:
        amount = CashBreakdown.objects.aggregate(Sum('amount'))
    One_thousands = amount['amount__sum'] // 1000 if amount['amount__sum'] else 0
    Five_hundreds = amount['amount__sum'] // 1000 // 500 if amount['amount__sum'] else 0
    Two_hundreds = amount['amount__sum'] // 1000 // 500 // 200 if amount['amount__sum'] else 0
    One_hundreds = amount['amount__sum'] // 1000 // 500 // 200 // 100 if amount['amount__sum'] else 0
    Fifties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 if amount['amount__sum'] else 0
    Forties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 if amount['amount__sum'] else 0
    Twenties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 if amount['amount__sum'] else 0
    Tens = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 if amount['amount__sum'] else 0
    Fives = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5 if amount[
        'amount__sum'] else 0
    Ones = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5 // 1 if amount[
        'amount__sum'] else 0

    context = {
        "note": CashBreakdown,
        "amount": amount,
        "One_th": One_thousands,
        "Five_hu": Five_hundreds,
        "Two_hu": Two_hundreds,
        "One_hu": One_hundreds,
        "Fifties_sh": Fifties,
        "Forties_sh": Forties,
        "Twenties_sh": Twenties,
        "Tens_sh": Tens,
        "Fives_sh": Fives,
        "Ones_sh": Ones,

    }

    return render(request, 'mogoon/cash_breakdown_update.html', context)


@never_cache
def CashBreakdownCreate(request):
    if request.method == "POST":
        cashBreakdown_date = request.POST['cashBreakdown_date']
        amount = request.POST['amount']
        One_thousands = request.POST['One_thousands']
        Five_hundreds = request.POST['Five_hundreds']
        Two_hundreds = request.POST['Two_hundreds']
        One_hundreds = request.POST['One_hundreds']
        Fifties = request.POST['Fifties']
        Forties = request.POST['Forties']
        Twenties = request.POST['Twenties']
        Tens = request.POST['Tens']
        Fives = request.POST['Fives']
        Ones = request.POST['Ones']

        insert = CashBreakdown(cashBreakdown_date=cashBreakdown_date, amount=amount, One_thousands=One_thousands,
                               Five_hundreds=Five_hundreds, Two_hundreds=Two_hundreds, One_hundreds=One_hundreds,
                               Fifties=Fifties, Forties=Forties, Twenties=Twenties, Tens=Tens, Fives=Fives, Ones=Ones)
        insert.save()
    return redirect('/cashBreakdown_table')


def CashBreakdownTotal(request):
    # calculate the change from each denomination
    note = CashBreakdown.objects.all()
    cashBreakdown_date = models.DateTimeField()
    amount = CashBreakdown.objects.aggregate(Sum('amount'))
    One_thousands = amount['amount__sum'] // 1000
    One_thousands_total = One_thousands * 1000
    Five_hundreds = amount['amount__sum'] // 1000 // 500
    Five_hundreds_total = Five_hundreds * 500
    Two_hundreds = amount['amount__sum'] // 1000 // 500 // 200
    Two_hundreds_total = Two_hundreds * 200
    One_hundreds = amount['amount__sum'] // 1000 // 500 // 200 // 100
    One_hundreds_total = One_hundreds * 100
    Fifties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50
    Fifties_total = Fifties * 50
    Forties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40
    Forties_total = Forties * 40
    Twenties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20
    Twenties_total = Twenties * 20
    Tens = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10
    Tens_total = Tens * 10
    Fives = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5
    Fives_total = Fives * 5
    Ones = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5 // 1
    Ones_total = Ones * 1

    context = {
        "cashBreakdown": note,
        "cashBreakdown_date": cashBreakdown_date,
        "amount": amount,
        "One_thousands": One_thousands,
        "One_thousands_total": One_thousands_total,
        "Five_hundreds": Five_hundreds,
        "Five_hundreds_total": Five_hundreds_total,
        "Two_hundreds": Two_hundreds,
        "Two_hundreds_total": Two_hundreds_total,
        "One_hundreds": One_hundreds,
        "One_hundreds_total": One_hundreds_total,
        "Fifties": Fifties,
        "Fifties_total": Fifties_total,
        "Forties": Forties,
        "Forties_total": Forties_total,
        "Twenties": Twenties,
        "Twenties_total": Twenties_total,
        "Tens": Tens,
        "Tens_total": Tens_total,
        "Fives": Fives,
        "Fives_total": Fives_total,
        "Ones": Ones,
        "Ones_total": Ones_total,

    }

    return render(request, 'mogoon/cashBreakdown_total.html', context)


def CashBreakdownEdit(request):
    # calculate the change from each denomination
    note = CashBreakdown.objects.all()
    cashBreakdown_date = models.DateTimeField()
    amount = CashBreakdown.objects.aggregate(Sum('amount'))

    if amount['amount__sum'] is not None:
        One_thousands = amount['amount__sum'] // 1000
        One_thousands_total = One_thousands * 1000
        Five_hundreds = amount['amount__sum'] // 1000 // 500
        Five_hundreds_total = Five_hundreds * 500
        Two_hundreds = amount['amount__sum'] // 1000 // 500 // 200
        Two_hundreds_total = Two_hundreds * 200
        One_hundreds = amount['amount__sum'] // 1000 // 500 // 200 // 100
        One_hundreds_total = One_hundreds * 100
        Fifties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50
        Fifties_total = Fifties * 50
        Forties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40
        Forties_total = Forties * 40
        Twenties = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20
        Twenties_total = Twenties * 20
        Tens = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10
        Tens_total = Tens * 10
        Fives = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5
        Fives_total = Fives * 5
        Ones = amount['amount__sum'] // 1000 // 500 // 200 // 100 // 50 // 40 // 20 // 10 // 5 // 1
        Ones_total = Ones * 1
    else:
        One_thousands = 0
        One_thousands_total = 0
        Five_hundreds = 0
        Five_hundreds_total = 0
        Two_hundreds = 0
        Two_hundreds_total = 0
        One_hundreds = 0
        One_hundreds_total = 0
        Fifties = 0
        Fifties_total = 0
        Forties = 0
        Forties_total = 0
        Twenties = 0
        Twenties_total = 0
        Tens = 0
        Tens_total = 0
        Fives = 0
        Fives_total = 0
        Ones = 0
        Ones_total = 0

    context = {
        "cashBreakdown": note,
        "cashBreakdown_date": cashBreakdown_date,
        "amount": amount,
        "One_thousands": One_thousands,
        "One_thousands_total": One_thousands_total,
        "Five_hundreds": Five_hundreds,
        "Five_hundreds_total": Five_hundreds_total,
        "Two_hundreds": Two_hundreds,
        "Two_hundreds_total": Two_hundreds_total,
        "One_hundreds": One_hundreds,
        "One_hundreds_total": One_hundreds_total,
        "Fifties": Fifties,
        "Fifties_total": Fifties_total,
        "Forties": Forties,
        "Forties_total": Forties_total,
        "Twenties": Twenties,
        "Twenties_total": Twenties_total,
        "Tens": Tens,
        "Tens_total": Tens_total,
        "Fives": Fives,
        "Fives_total": Fives_total,
        "Ones": Ones,
        "Ones_total": Ones_total,

    }
    return render(request, 'mogoon/cash_breakdown_update.html', context)


@never_cache
def CashBreakdownEditCreate(request):
    if request.method == "POST":
        cashBreakdown_date = request.POST['cashBreakdown_date']
        amount = request.POST['amount']
        One_thousands = request.POST['One_thousands']
        Five_hundreds = request.POST['Five_hundreds']
        Two_hundreds = request.POST['Two_hundreds']
        One_hundreds = request.POST['One_hundreds']
        Fifties = request.POST['Fifties']
        Forties = request.POST['Forties']
        Twenties = request.POST['Twenties']
        Tens = request.POST['Tens']
        Fives = request.POST['Fives']
        Ones = request.POST['Ones']

        insert = CashBreakdown(cashBreakdown_date=cashBreakdown_date, amount=amount, One_thousands=One_thousands,
                               Five_hundreds=Five_hundreds, Two_hundreds=Two_hundreds, One_hundreds=One_hundreds,
                               Fifties=Fifties, Forties=Forties, Twenties=Twenties, Tens=Tens, Fives=Fives, Ones=Ones)
        insert.save()
    return redirect('/cashBreakdown_updateEdit')


def CashBreakdown_update(request):
    if request.method == 'POST':
        form = CashBreakdownForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            results = []
            denominations = [1000, 500, 200, 100, 50, 40, 20, 10, 5, 1]
            for denomination in denominations:
                count = amount // denomination
                amount = amount % denomination
                results.append({
                    'amount': denomination,
                    'count': count
                })
            return render(request, 'mogoon/cash_breakdown_create_table.html', {'results': results})
    else:
        form = CashBreakdownForm()
    return render(request, 'mogoon/cash_breakdown_update.html', {'form': form})


def CashBreakdown_create(request):
    if request.method == 'POST':
        form = CashBreakdownForm(request.POST)
        if form.is_valid():
            cashBreakdown = form.save()
            cashBreakdown.save()
            messages.success(request, 'Cash Breakdown successfully created')
            return redirect('cash_breakdown_create')
    else:
        form = CashBreakdownForm()
    return render(request, 'mogoon/cash_breakdown_create_table.html', {'form': form})


def calculateTotals(request):
    amount = request.POST.get('amount', 0)
    One_th = request.POST.get('One_th', 0)
    Five_hu = request.POST.get('Five_hu', 0)
    Two_hu = request.POST.get('Two_hu', 0)
    One_hu = request.POST.get('One_hu', 0)
    Fifties_sh = request.POST.get('Fifties_sh', 0)
    Forties_sh = request.POST.get('Forties_sh', 0)
    Twenties_sh = request.POST.get('Twenties_sh', 0)
    Tens_sh = request.POST.get('Tens_sh', 0)
    Fives_sh = request.POST.get('Fives_sh', 0)
    Ones_sh = request.POST.get('Ones_sh', 0)

    one_thousand_total = int(One_th) * 1000
    five_hundred_total = int(Five_hu) * 500
    two_hundred_total = int(Two_hu) * 200
    one_hundred_total = int(One_hu) * 100
    fifties_total = int(Fifties_sh) * 50
    forties_total = int(Forties_sh) * 40
    twenties_total = int(Twenties_sh) * 20
    tens_total = int(Tens_sh) * 10
    fives_total = int(Fives_sh) * 5
    ones_total = int(Ones_sh) * 1

    amount_total = amount * 1
    grand_total = one_thousand_total + five_hundred_total + two_hundred_total + one_hundred_total + fifties_total \
                  + forties_total + twenties_total + tens_total + fives_total + ones_total

    context = {
        'amount_total': amount_total,
        'One_thousands_total': one_thousand_total,
        'Five_hundreds_total': five_hundred_total,
        'Two_hundreds_total': two_hundred_total,
        'One_hundreds_total': one_hundred_total,
        'Fifties_total': fifties_total,
        'Forties_total': forties_total,
        'Twenties_total': twenties_total,
        'Tens_total': tens_total,
        'Fives_total': fives_total,
        'Ones_total': ones_total,
        'total': grand_total
    }

    return render(request, 'mogoon/cashBreakdown_total.html', context)


def calculate_coin_totals(amount, One_th, Five_hu, Two_hu, One_hu, Fifties_sh, Forties_sh, Twenties_sh, Tens_sh,
                          Fives_sh, Ones_sh):
    one_thousand_total = One_th.value * 1000
    five_hundred_total = Five_hu.value * 500
    two_hundred_total = Two_hu.value * 200
    one_hundred_total = One_hu.value * 100
    fifties_total = Fifties_sh.value * 50
    forties_total = Forties_sh.value * 40
    twenties_total = Twenties_sh.value * 20
    tens_total = Tens_sh.value * 10
    fives_total = Fives_sh.value * 5
    ones_total = Ones_sh.value * 1
    total = one_thousand_total + five_hundred_total + two_hundred_total + one_hundred_total + fifties_total + forties_total + twenties_total + tens_total + fives_total + ones_total

    return {
        'amount': amount.value,
        'One_thousand': One_th.value,
        'Five_hundred': Five_hu.value,
        'Two_hundred': Two_hu.value,
        'One_hundred': One_hu.value,
        'Fifties': Fifties_sh.value,
        'Forties': Forties_sh.value,
        'Twenties': Twenties_sh.value,
        'Tens': Tens_sh.value,
        'Fives': Fives_sh.value,
        'Ones': Ones_sh.value,
        'total': total
    }


# CRUD functionality for the tables
@login_required(login_url='login')
@never_cache
def update(request, pk):
    data = Crop.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/crop_table')

    else:
        form = UpdateTaskForm(instance=data)

    context = {
        'form': form, 'UpdateTaskForm': UpdateTaskForm,

    }
    return render(request, 'Crop_data/update.html', context)


@login_required(login_url='login')
@never_cache
def delete(request, pk):
    data = Crop.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/crop_table')

    context = {
        'item': data,
    }
    return render(request, 'Crop_data/delete.html', context)


@login_required(login_url='login')
@never_cache
def F_update(request, pk):
    data = Fertilizer.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateFertilizerForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/fertilizer_table')

    else:
        form = UpdateFertilizerForm(instance=data)

    context = {
        'form': form, 'UpdateFertilizerForm': UpdateFertilizerForm,

    }
    return render(request, 'Fertilizer/update.html', context)


@login_required(login_url='login')
@never_cache
def F_delete(request, pk):
    data = Fertilizer.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/fertilizer_table')

    context = {
        'item': data,
    }
    return render(request, 'Fertilizer/delete.html', context)


@login_required(login_url='login')
@never_cache
def K_update(request, pk):
    data = Kandojobs.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateKandojobsForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/kandojobs_table')

    else:
        form = UpdateKandojobsForm(instance=data)

    context = {
        'form': form, 'UpdateKandojobsForm': UpdateKandojobsForm,

    }
    return render(request, 'Kandojobs/update.html', context)


@login_required(login_url='login')
@never_cache
def K_delete(request, pk):
    data = Kandojobs.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/kandojobs_table')

    context = {
        'item': data,
    }
    return render(request, 'Kandojobs/delete.html', context)


@login_required(login_url='login')
@never_cache
def M_update(request, pk):
    data = Milk.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateMilkForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/milk_table')

    else:
        form = UpdateMilkForm(instance=data)

    context = {
        'form': form, 'UpdateMilkForm': UpdateMilkForm,

    }
    return render(request, 'Milk/update.html', context)


@login_required(login_url='login')
@never_cache
def M_delete(request, pk):
    data = Milk.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/milk_table')

    context = {
        'item': data,
    }
    return render(request, 'Milk/delete.html', context)


@login_required(login_url='login')
@login_required
def P_update(request, pk):
    data = CropP.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/purple_table')

    else:
        form = UpdateTaskForm(instance=data)

    context = {
        'form': form, 'UpdateTaskForm': UpdateTaskForm,

    }
    return render(request, 'Purple/update.html', context)


@login_required(login_url='login')
@login_required
def P_delete(request, pk):
    data = CropP.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/purple_table')

    context = {
        'item': data,
    }
    return render(request, 'Purple/delete.html', context)


@never_cache
def C_update(request, pk):
    note = CashBreakdown.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateCashBreakdownForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('/cashBreakdown_table')

    else:
        form = UpdateCashBreakdownForm(instance=note)

    context = {
        'form': form, 'UpdateCashBreakdownForm': UpdateCashBreakdownForm,

    }
    return render(request, 'cashBreakdown/update.html', context)


@never_cache
def C_delete(request, pk):
    note = CashBreakdown.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('/cashBreakdown_table')

    context = {
        'item': note,
    }
    return render(request, 'cashBreakdown/delete.html', context)


def R_update(request, pk):
    note = CashBreakdown.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateCashBreakdownForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return redirect('/mogoon-cashBreakdown_edit')

    else:
        form = UpdateCashBreakdownForm(instance=note)

    context = {
        'form': form, 'UpdateCashBreakdownForm': UpdateCashBreakdownForm,

    }
    return render(request, 'cashBreakdown_edit/Edit_update.html', context)


def R_delete(request, pk):
    note = CashBreakdown.objects.get(id=pk)
    if request.method == 'POST':
        note.delete()
        return redirect('/mogoon-cashBreakdown_edit')

    context = {
        'item': note,
    }
    return render(request, 'cashBreakdown_edit/Edit_delete.html', context)
