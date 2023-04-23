import datetime
from decimal import Decimal

import pytz
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db.models import Sum, F, Count, Avg, FloatField
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache

from . import models
from .forms import TaskForms, UpdateTaskForm, UpdatePurpleForm, UpdateFertilizerForm, UpdateKandojobsForm, \
    UpdateMilkForm, EmployeeForm, EmployeeDetailsForm
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


@login_required(login_url='login')
@never_cache
def Reports(request):
    context = {
        "name": {"Reports Farm Page"},
        'form': TaskForms
    }
    return render(request, 'mogoon/reports.html', context)


def Employee_list(request):
    employee_list = Employee.objects.all()
    return render(request, 'mogoon/employee_list.html', {'employee_list': employee_list})


@never_cache
def Employee_update(request, pk):
    employee_list = Employee.objects.all()
    employee = Employee.objects.get(id=pk)
    date_employed = models.DateTimeField()
    salary = Employee.objects.aggregate(sal_count=Count('salary'))
    total = Employee.objects.aggregate(sal_total=Sum('salary'))
    form = EmployeeForm(instance=employee)
    if salary.get('sal_count') is None:
        salary['sal_count'] = 0
    else:
        salary = Employee.objects.aggregate(sal_count=Count('salary'))

    if total.get('sal_total') is None:
        total['sal_total'] = 0
    else:
        total = Employee.objects.aggregate(sal_total=Sum('salary'))

    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-details', pk=pk)
    context = {'form': form}
    return render(request, 'mogoon/employee_details_update.html', context)


@never_cache
def Employee_details(request):
    employee = Employee.objects.all()
    date_employed = models.DateTimeField()
    salary = Employee.objects.aggregate(sal_count=Count('salary'))
    total = Employee.objects.aggregate(sal_total=Sum('salary'))

    if request.method == "POST":
        employee_form = EmployeeForm(request.POST)
        if employee_form.is_valid():
            # Create or update Employee object
            date_employed = employee_form.cleaned_data['date_employed']
            national_identity = employee_form.cleaned_data['national_identity']
            employee, created = Employee.objects.update_or_create(date_employed=date_employed,
                                                                  national_identity=national_identity,
                                                                  defaults=employee_form.cleaned_data)

            # Show appropriate message based on whether object was created or updated
            if created:
                messages.success(request, 'Employee details are successfully saved.')
            else:
                messages.success(request, 'Employee details are successfully updated.')

            return redirect('employee-list')
    else:
        employee_form = EmployeeForm()

    return render(request, 'mogoon/employee_details_update.html',
                  {'employee_form': employee_form, 'employee': employee, 'date_employed': date_employed,
                   'salary': salary, 'total': total})


def Employee_create(request):
    employee_list = Employee.objects.all()
    return render(request, 'mogoon/employee_create.html', {'employee_list': employee_list})


@never_cache
def GreenTable(request):
    data = Green.objects.all()
    plucking_date = models.DateTimeField()
    green_today = Green.objects.aggregate(all_count=Count('green_today'))
    green_todate_result = Green.objects.aggregate(all_sum=Sum('green_today'))
    total_pluckers_result = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucker_numbers = Green.objects.aggregate(all_count=Count('plucker_numbers'))
    plucking_average = Green.objects.aggregate(pl_ave=Avg(F('green_todate') / F('total_pluckers')))

    green_todate = green_todate_result['all_sum'] if green_todate_result['all_sum'] is not None else 0
    total_pluckers = total_pluckers_result['pl_total'] if total_pluckers_result['pl_total'] is not None else 1
    plucking_average = Green.objects.aggregate(pl_ave=Avg('green_todate', output_field=FloatField()))[
        'pl_ave'] if total_pluckers != 0 else 0

    total_green = Green.objects.aggregate(total_sum=Sum('green_todate'))

    context = {
        "green_data": data,
        "plucking_date": plucking_date,
        "c_today": green_today,
        "c_todate": green_todate,
        "p_numbers": plucker_numbers,
        "t_pluckers": total_pluckers,
        "p_average": plucking_average,
        "t_green": total_green,
    }
    return render(request, 'mogoon/green_table.html', context)


"""What changed in the code?

The code was changed to match the template. The code was modified to include the data from the green model and to 
calculate the necessary values to display on the template. The code was also modified to handle scenarios where the 
database is empty and the values are returned as None. This was done by checking the value of the all_sum key in the 
green_todate dictionary and setting it to 0 if it is of type None. This allows the template to display the 0 value 
instead of None. Other changes include adding variables for plucker_numbers, total_pluckers, plucking_average and 
total_green. These variables are used to calculate the necessary values to display on the template. """


@login_required(login_url='login')
@never_cache
def GreenTableUpdate(request):
    green_today = Green.objects.count()
    # get the current green_todate value
    green_todate = Green.objects.aggregate(all_sum=Sum('green_today'))
    # the green_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is null as shown below, when null is set to type None and not type
    # Null
    if green_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        green_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the green_todate and pass it to the templates via the context, this value
        # appears in the form
        green_todate = Green.objects.aggregate(all_sum=Sum('green_today'))
    plucker_numbers = Green.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))
    if total_pluckers.get('pl_total') is None:
        total_pluckers['pl_total'] = 0
    else:
        total_pluckers = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))

    if total_pluckers.get('pl_total') == 0:
        plucking_average = 0
    else:
        plucking_average = Green.objects.aggregate(pl_ave=Avg('green_todate') / total_pluckers.get('pl_total'))
        plucking_average = plucking_average.get('pl_ave') if total_pluckers.get('pl_total') != 0 else 0

    total_green = Green.objects.aggregate(total_sum=Sum('green_todate'))
    if total_green.get('total_sum') is None:
        total_green['total_sum'] = 0
    else:
        total_green = Green.objects.aggregate(total_sum=Sum('green_todate'))

    context = {
        "green_today": green_today,
        "green_todate": green_todate,
        "plucker_numbers": plucker_numbers,
        "total_pluckers": total_pluckers,
        "plucking_average": plucking_average,
        "total_green": total_green,

    }
    return render(request, 'mogoon/green_table_update.html', context)


@login_required(login_url='login')
@never_cache
def mogoonGreenCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The green_todate is the green todate gotten from the
        # form(that was passed from the notes function) plus the green today entered in the form. Initially the green
        # to date is zero when the dta base is empty. the new green to date will be zero plus the green today entered
        # in the form, this addition is inserted and saved in the database as green todate as shown below.
        plucking_date = request.POST['plucking_date']
        green_data = request.POST['green_data']
        green_today = request.POST['green_today']
        # Initially request.POST['green_today'] is a string, it has to be wrapped with an int for purpose of addition
        green_todate = int(request.POST['green_todate']) + int(green_today)
        plucker_numbers = request.POST['plucker_number']
        total_pluckers = request.POST['total_pluckers']
        plucking_average = float(request.POST['plucking_average'])
        total_green = request.POST['total_green']

        insert = Green(plucking_date=plucking_date, green_data=green_data, green_today=green_today,
                       green_todate=green_todate,
                       plucker_numbers=plucker_numbers, total_pluckers=total_pluckers,
                       plucking_average=plucking_average,
                       total_green=total_green)
        insert.save()

    return redirect('/green_table')


@never_cache
def PurpleTable(request):
    data = Purple.objects.all()
    plucking_date = models.DateTimeField()
    purple_today = Purple.objects.aggregate(all_count=Count('purple_today'))
    purple_todate_result = Purple.objects.aggregate(all_sum=Sum('purple_today'))
    total_pluckers_result = Purple.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucker_numbers = Purple.objects.aggregate(all_count=Count('plucker_numbers'))
    plucking_average = Purple.objects.aggregate(pl_ave=Avg(F('purple_todate') / F('total_pluckers')))

    purple_todate = purple_todate_result['all_sum'] if purple_todate_result['all_sum'] is not None else 0
    total_pluckers = total_pluckers_result['pl_total'] if total_pluckers_result['pl_total'] is not None else 1
    plucking_average = Purple.objects.aggregate(pl_ave=Avg('purple_todate', output_field=FloatField()))[
        'pl_ave'] if total_pluckers != 0 else 0

    total_purple = Purple.objects.aggregate(total_sum=Sum('purple_todate'))
    context = {
        "purple_data": data,
        "plucking_date": plucking_date,
        "cs_today": purple_today,
        "cs_todate": purple_todate,
        "ps_numbers": plucker_numbers,
        "ts_total": total_pluckers,
        "ps_average": plucking_average,
        "t_purple": total_purple,

    }
    return render(request, 'mogoon/purple_tea.html', context)


# raise Exception("I want to know value" + str("purple Table"))

@login_required(login_url='login')
@never_cache
def PurpleTableUpdate(request):
    purple_today = Purple.objects.count()
    # get the current purple_todate value
    purple_todate = Purple.objects.aggregate(all_sum=Sum('purple_today'))
    # the purple_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is null as shown below, when null is set to type None and not type
    # Null
    if purple_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        purple_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the purple_todate and pass it to the templates via the context, this value
        # appears in the form
        purple_todate = Purple.objects.aggregate(all_sum=Sum('purple_today'))
    plucker_numbers = Purple.objects.aggregate(all_count=Count('plucker_numbers'))
    total_pluckers = Purple.objects.aggregate(pl_total=Sum('plucker_numbers'))
    if total_pluckers.get('pl_total') is None:
        total_pluckers['pl_total'] = 0
    else:
        total_pluckers = Purple.objects.aggregate(pl_total=Sum('plucker_numbers'))

    if total_pluckers.get('pl_total') == 0:
        plucking_average = 0
    else:
        plucking_average = Purple.objects.aggregate(pl_ave=Avg('purple_todate') / total_pluckers.get('pl_total'))
        plucking_average = plucking_average.get('pl_ave') if total_pluckers.get('pl_total') != 0 else 0

    total_purple = Purple.objects.aggregate(total_sum=Sum('purple_todate'))
    if total_purple.get('total_sum') is None:
        total_purple['total_sum'] = 0
    else:
        total_purple = Purple.objects.aggregate(total_sum=Sum('purple_todate'))

    context = {
        "purple_today": purple_today,
        "purple_todate": purple_todate,
        "plucker_numbers": plucker_numbers,
        "total_pluckers": total_pluckers,
        "plucking_average": plucking_average,
        "total_purple": total_purple,

    }
    return render(request, 'mogoon/purple_tea_update.html', context)


@login_required(login_url='login')
@never_cache
def PurpleCreate(request):
    if request.method == "POST":
        # this function saves a new record from the notes form. The purple_todate is the purple todate gotten from
        # the form(that was passed from the notes function) plus the purple today entered in the form. Initially the
        # purple to date is zero when the dta base is empty. the new purple to date will be zero plus the purple
        # today entered in the form, this addition is inserted and saved in the database as purple todate as shown
        # below.
        plucking_date = request.POST['plucking_date']
        purple_data = request.POST['purple_data']
        purple_today = request.POST['purple_today']
        # Initially request.POST['purple_today'] is a string, it has to be wrapped with an int for purpose of addition
        purple_todate = int(request.POST['purple_todate']) + int(purple_today)
        plucker_numbers = request.POST['plucker_number']
        total_pluckers = request.POST['total_pluckers']
        plucking_average = float(request.POST['plucking_average'])
        total_purple = request.POST['total_purple']

        insert = Purple(plucking_date=plucking_date, purple_data=purple_data, purple_today=purple_today,
                        purple_todate=purple_todate,
                        plucker_numbers=plucker_numbers, total_pluckers=total_pluckers,
                        plucking_average=plucking_average,
                        total_purple=total_purple)
        insert.save()

    return redirect('/purple_table')


@never_cache
def KandojobsTable(request):
    data = Kandojobs.objects.all()
    pruned_bushes = Kandojobs.objects.aggregate(pr_count=Count('pruned_bushes'))
    total_pruned_bushes = Kandojobs.objects.aggregate(pr_sum=Sum('pruned_bushes'))
    pruning_rate = Decimal(request.GET.get('pruning_rate', 0))
    pruning_cost = pruned_bushes.get('pr_count') * pruning_rate
    weeding_chem_amt = Kandojobs.objects.aggregate(wc_sum=Sum('weeding_chem_amt'))
    total_chem_amt = weeding_chem_amt.get('wc_sum', 0) or 0
    kandojob = Kandojobs.objects.first()
    cost_per_lit = kandojob.cost_per_lit if kandojob else 0
    if kandojob:
        cost_per_lit = kandojob.cost_per_lit
    else:
        cost_per_lit = 0
    weeding_labour_number = Kandojobs.objects.aggregate(wl_sum=Sum('weeding_labour_number'))
    total_weeding_labour_number = weeding_labour_number.get('wl_sum', 0) or 0
    weeding_labour_rate = Decimal(request.GET.get('weeding_labour_rate', 0))
    weeding_labour = total_weeding_labour_number * weeding_labour_rate
    weeding_cost = (total_chem_amt * cost_per_lit) + weeding_labour

    context = {
        "kandojobs": data,
        "pr_count": pruned_bushes.get('pr_count', 0),
        "pr_sum": total_pruned_bushes.get('pr_sum', 0),
        "pruning_rate": pruning_rate,
        "pruning_cost": pruning_cost,
        "total_chem_amt": total_chem_amt,
        "cost_per_lit": cost_per_lit,
        "total_weeding_labour_number": total_weeding_labour_number,
        "weeding_labour_rate": weeding_labour_rate,
        "weeding_labour": weeding_labour,
        "weeding_cost": weeding_cost,
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
        # form(that was passed from the notes function) plus the Milk today entered in the form. Initially the green
        # to date is zero when the dta base is empty. the new Milk to date will be zero plus the green today entered
        # in the form, this addition is inserted and saved in the database as green todate as shown below.
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


# CRUD functionality for the tables
@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
@never_cache
def update(request, pk):
    data = Green.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/green_table')

    else:
        form = UpdateTaskForm(instance=data)

    context = {
        'form': form, 'UpdateTaskForm': UpdateTaskForm,

    }
    return render(request, 'Green/update.html', context)


@login_required(login_url='login')
@never_cache
def delete(request, pk):
    data = Green.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/green_table')

    context = {
        'item': data,
    }
    return render(request, 'Green/delete.html', context)


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
    data = Purple.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdatePurpleForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/purple_table')

    else:
        form = UpdatePurpleForm(instance=data)

    context = {
        'form': form, 'UpdatePurpleForm': UpdatePurpleForm,

    }
    return render(request, 'Purple/update.html', context)


@login_required(login_url='login')
@login_required
def P_delete(request, pk):
    data = Purple.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/purple_table')

    context = {
        'item': data,
    }
    return render(request, 'Purple/delete.html', context)
