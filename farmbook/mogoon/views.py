import datetime
import logging
from decimal import Decimal

import pytz
from django.contrib.auth.decorators import login_required
from django.core.checks import messages
from django.db.models import Sum, F, Count, Avg, Min, ExpressionWrapper, DecimalField
from django.db.models.functions import Cast
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.views.decorators.cache import never_cache
from pytz import UTC
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from .forms import UpdateGreenForm, UpdatePurpleForm, UpdateFertilizerForm, UpdateKandojobsForm, \
    UpdateMilkForm, EmployeeForm, ReportsForm
from .models import *
from .models import Employee
from .models import Milk
from .serializer import GreenSerializer, PurpleSerializer, KandojobsSerializer, FertilizerSerializer, MilkSerializer, \
    EmployeeSerializer, ReportsSerializer

logger = logging.getLogger(__name__)


# Create your views here.
@login_required(login_url='login')
@never_cache
def reports_view_retrieve(request):
    reports = Reports.objects.all()
    form = ReportsForm()

    context = {
        "name": "Reports Page",  # Remove unnecessary curly braces
        'reports': reports,
        "ReportsForm": form,  # Pass the form instance
    }
    return render(request, 'mogoon/view_reports.html', context)


@login_required(login_url='login')
@never_cache
def reports_view_fetch_details(request):
    if request.method == "POST":
        form = ReportsForm(request.POST, request.FILES)
        if form.is_valid():
            # Assuming your form has fields like daily_report, visitors_name, etc.
            daily_report = form.cleaned_data['daily_report']
            visitors_name = form.cleaned_data['visitors_name']
            visitor_comments = form.cleaned_data['visitor_comments']
            farm_report = form.cleaned_data['farm_report']
            farm_requirements = form.cleaned_data['farm_requirements']
            farm_image = form.cleaned_data['farm_image']

            context = {
                "daily_report": daily_report,
                "visitors_name": visitors_name,
                "visitor_comments": visitor_comments,
                "farm_report": farm_report,
                "farm_requirements": farm_requirements,
                "farm_image": farm_image,
            }
            return render(request, 'mogoon/reports_create.html', context)
    else:
        form = ReportsForm()

    context = {
        'form': form,
    }
    return render(request, 'mogoon/reports_create.html', context)


@login_required(login_url='login')
@never_cache
def reports_view_create(request):
    if request.method == 'POST':
        form = ReportsForm(request.POST, request.FILES)
        if form.is_valid():
            # Access cleaned data, including the file, from the form
            daily_report = form.cleaned_data['daily_report']
            visitors_name = form.cleaned_data['visitors_name']
            visitor_comments = form.cleaned_data['visitor_comments']
            farm_report = form.cleaned_data['farm_report']
            farm_requirements = form.cleaned_data['farm_requirements']
            farm_image = form.cleaned_data['farm_image']

            # Create and save the Reports object
            insert = Reports(
                daily_report=daily_report,
                visitors_name=visitors_name,
                visitor_comments=visitor_comments,
                farm_report=farm_report,
                farm_requirements=farm_requirements,
                farm_image=farm_image
            )
            insert.save()

            return redirect('/')
    else:
        form = ReportsForm()

    return render(request, 'mogoon/view_reports.html', {'form': form})


def graphs_view(request):
    # Retrieve data from various models
    employees_data = Employee.objects.all()
    green_data = Green.objects.all()
    purple_data = Purple.objects.all()
    kandojobs_data = Kandojobs.objects.all()
    fertilizer_data = Fertilizer.objects.all()
    milk_data = Milk.objects.all()

    # Use specific forms for each model
    employee_form = EmployeeForm(request.POST or None)
    green_form = UpdateGreenForm(request.POST or None)
    purple_form = UpdatePurpleForm(request.POST or None)
    kandojobs_form = UpdateKandojobsForm(request.POST or None)
    fertilizer_form = UpdateFertilizerForm(request.POST or None)
    milk_form = UpdateMilkForm(request.POST or None)

    # Combine data and forms into a dictionary
    data_and_forms = {
        'Employees': {'data': employees_data, 'form': employee_form},
        'Green': {'data': green_data, 'form': green_form},
        'Purple': {'data': purple_data, 'form': purple_form},
        'Kandojobs': {'data': kandojobs_data, 'form': kandojobs_form},
        'Fertilizer': {'data': fertilizer_data, 'form': fertilizer_form},
        'Milk': {'data': milk_data, 'form': milk_form},
    }

    if request.method == 'POST':
        # Determine the form submitted and handle it accordingly
        form_name = request.POST.get('form_name')
        if form_name in data_and_forms:
            current_form = data_and_forms[form_name]['form']
            if current_form.is_valid():
                current_form.save()

    context = {
        'name': 'This is the graphs dashboard',
        'data_and_forms': data_and_forms,
    }

    return render(request, 'mogoon/graphs.html', context)


@never_cache
def employee_view_retrieve(request):
    # Query all employees from the database
    employee_data = Employee.objects.all()
    form = EmployeeForm()

    # Calculate the total salary of all employees
    salary_total = Employee.objects.aggregate(sal_add=Count('salary_total'))['sal_add'] or 0

    # Calculate the sum and average salary of all employees
    salary_sum = Employee.objects.aggregate(salary_sum=Sum('salary_total'))['salary_sum'] or 0
    salary_avg = Employee.objects.aggregate(salary_avg=Avg('salary_total'))['salary_avg'] or 0

    # Count the number of employees
    no_employees = Employee.objects.count()

    # Define the context dictionary with all the data
    context = {
        "employee_data": employee_data,
        "form": form,

    }

    # Render the template with the context data
    return render(request, 'mogoon/employee_list.html', context)


@never_cache
def employee_view_fetch_details(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee-list')  # Redirect to the employee list page after successful form submission
    else:
        form = EmployeeForm()

    # Calculate the total salary and Average of all employees
    salary_total = Employee.objects.aggregate(sal_add=Count('salary_total'))['sal_add'] or 0

    # Calculate the sum and average salary of all employees
    salary_sum = Employee.objects.aggregate(salary_sum=Sum('salary_total'))['salary_sum'] or 0
    salary_avg = Employee.objects.aggregate(salary_avg=Avg('salary_total'))['salary_avg'] or 0

    # Count the number of employees
    total_count = Employee.objects.count()

    context = {
        'form': form,
        'sal_add': salary_total,
        'salary_sum': salary_sum,
        'salary_avg': salary_avg,
        'no_employees': total_count,
    }

    return render(request, 'mogoon/employee_details_create.html', context)


@login_required(login_url='login')
@never_cache
def employee_view_create(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = EmployeeForm()

        date_employed = request.POST['date_employed']
        national_identity = request.POST['national_identity']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST.get('gender', False)
        department = request.POST.get('department', False)
        position = request.POST.get('position', False)
        salary_total = request.POST['salary_total']

        insert = Employee(date_employed=date_employed, national_identity=national_identity, name=name, age=age,
                          gender=gender, department=department, position=position, salary_total=salary_total)
        insert.save()

        return redirect('/employee-list')


@never_cache
def green_view_retrieve(request):
    data = Green.objects.all()
    plucking_date = Green._meta.get_field('plucking_date').verbose_name

    green_today = Green.objects.aggregate(all_count=Count('green_today'))
    green_todate_result = Green.objects.aggregate(all_sum=Sum('green_today'))
    total_pluckers_result = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucker_numbers = Green.objects.aggregate(all_count=Count('plucker_numbers'))
    green_todate = green_todate_result['all_sum'] if green_todate_result['all_sum'] is not None else 0
    total_pluckers = total_pluckers_result['pl_total'] if total_pluckers_result['pl_total'] is not None else 1

    # Calculate the plucking average
    plucking_average = Green.objects.aggregate(
        pl_ave=Avg(F('green_today') / F('plucker_numbers'), output_field=models.FloatField())
    )['pl_ave'] if total_pluckers != 0 else 0

    total_green = Green.objects.aggregate(total_sum=Sum('green_today'))

    context = {
        "green_data": data,
        "plucking_date": plucking_date,
        "c_today": green_today['all_count'],
        "c_todate": green_todate,
        "p_numbers": plucker_numbers['all_count'],
        "t_pluckers": total_pluckers,
        "p_average": plucking_average,
        "t_green": total_green['total_sum'],
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
def green_view_fetch_details(request):
    data = Green.objects.all()
    if request.method == 'POST':
        form = UpdateGreenForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = UpdateGreenForm()
    green_today = Green.objects.count()
    # get the current green_todate value
    green_todate = Green.objects.aggregate(all_sum=Sum('green_today'))
    # the green_todate variable is a dictionary with a key value pair, the key is all_sum as set above,
    # when the database is empty the value of all_sum is set to python type called None, to cater for this scenario
    # get the value of the all_sum and check if it is null as shown below, when null is set to type None and not type
    # Null
    plucker_numbers = Green.objects.aggregate(all_count=Count('plucker_numbers'))
    if green_todate.get('all_sum') is None:
        # if the value is of type None set the value to zero because this value is used later for additions and a none
        # type cannot be added to the int type
        green_todate['all_sum'] = 0
        # this value appears in the form as 0 instead of 'None'
    else:
        # if it has an actual value get the green_todate and pass it to the templates via the context, this value
        # appears in the form
        green_todate = Green.objects.aggregate(all_sum=Sum('green_today'))
    total_pluckers = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))

    if total_pluckers.get('pl_total') is None:
        total_pluckers['pl_total'] = 0
    else:
        total_pluckers = Green.objects.aggregate(pl_total=Sum('plucker_numbers'))

    if total_pluckers.get('pl_total') == 0:
        plucking_average = 0
    else:
        # plucking_average = Green.objects.aggregate(pl_ave=Avg('green_todate') / total_pluckers.get('pl_total'))
        plucking_average = Green.objects.aggregate(
            pl_ave=Avg(F('green_today') / F('plucker_numbers'), output_field=models.FloatField())
        )['pl_ave'] if total_pluckers != 0 else 0
    #     plucking_average = plucking_average.get('pl_ave') if total_pluckers.get('pl_total') != 0 else 0
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
    return render(request, 'mogoon/green_table_create.html', context)


@login_required(login_url='login')
@never_cache
def green_view_create(request):
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
def purple_view_retrieve(request):
    data = Purple.objects.all()
    plucking_date = Purple._meta.get_field('plucking_date').verbose_name

    purple_today = Purple.objects.aggregate(all_count=Count('purple_today'))
    purple_todate_result = Purple.objects.aggregate(all_sum=Sum('purple_today'))
    total_pluckers_result = Purple.objects.aggregate(pl_total=Sum('plucker_numbers'))
    plucker_numbers = Purple.objects.aggregate(all_count=Count('plucker_numbers'))
    purple_todate = purple_todate_result['all_sum'] if purple_todate_result['all_sum'] is not None else 0
    total_pluckers = total_pluckers_result['pl_total'] if total_pluckers_result['pl_total'] is not None else 1

    # Calculate the plucking average
    plucking_average = Purple.objects.aggregate(
        pl_ave=Avg(F('purple_today') / F('plucker_numbers'), output_field=models.FloatField())
    )['pl_ave'] if total_pluckers != 0 else 0

    total_purple = Purple.objects.aggregate(total_sum=Sum('purple_today'))

    context = {
        "purple_data": data,
        "plucking_date": plucking_date,
        "c_today": purple_today['all_count'],
        "c_todate": purple_todate,
        "p_numbers": plucker_numbers['all_count'],
        "t_pluckers": total_pluckers,
        "p_average": plucking_average,
        "t_purple": total_purple['total_sum'],
    }
    return render(request, 'mogoon/purple_tea.html', context)


# raise Exception("I want to know value" + str("purple Table"))

@login_required(login_url='login')
@never_cache
def purple_view_fetch_details(request):
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
        plucking_average = Purple.objects.aggregate(
            pl_ave=Avg(F('purple_today') / F('plucker_numbers'), output_field=models.FloatField())
        )['pl_ave'] if total_pluckers != 0 else 0

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
    return render(request, 'mogoon/purple_tea_create.html', context)


@login_required(login_url='login')
@never_cache
def purple_view_create(request):
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
def kandojobs_view_retrieve(request):
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
def kandojobs_view_fetch_details(request):
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
    return render(request, 'mogoon/kandojobs_table_create.html', context)


@login_required(login_url='login')
@never_cache
def kandojobs_view_create(request):
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
def milk_view_retrieve(request):
    data = Milk.objects.all()
    milking_done = Milk._meta.get_field('milking_done').verbose_name
    today = now().date()
    milk_today = Milk.objects.filter(milking_done__date=today)
    total = milk_today.aggregate(sum_total=Sum('milk_today'))['sum_total'] if milk_today != 0 else 0
    milk_todate = Milk.objects.aggregate(all_sum=Sum('milk_today'))
    cows_milked = Milk.objects.aggregate(all_sum=Sum('cows_milked'))
    cow_numbers = Milk.objects.aggregate(all_sum=Sum('cow_numbers'))

    # Calculate the milking average
    milking_average = Milk.objects.aggregate(
        ml_ave=Avg(F('milk_today') / F('cows_milked'), output_field=models.FloatField())
    )['ml_ave'] if cow_numbers != 0 else 0

    total_milk = Milk.objects.aggregate(total_sum=Sum('milk_today'))
    calf_down = datetime.now(tz=UTC).replace(tzinfo=None)
    today = datetime.utcnow()
    calf_age = today - calf_down
    calf_numbers = Milk.objects.count()
    vet_cost = Milk.objects.aggregate(all_sum=Sum('vet_cost'))
    Total_vet_cost = Milk.objects.aggregate(total_cost=Sum('vet_cost'))

    context = {
        "Milk": data,
        "m_done": milking_done,
        "m_today": total,
        "m_todate": milk_todate['all_sum'],
        "c_milked": cows_milked,
        "c_numbers": cow_numbers,
        "m_average": milking_average,
        "t_milk": total_milk['total_sum'],
        "today": today,
        "cf_down": calf_down,
        "cf_age": calf_age,
        "cf_numbers": calf_numbers,
        "v_cost": vet_cost,
        "T_v_cost": Total_vet_cost['total_cost'],
    }
    print(milk_today)
    return render(request, 'mogoon/milk_table.html', context)


@login_required(login_url='login')
@never_cache
def milk_view_fetch_details(request):
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
    milking_average = Milk.objects.aggregate(
        ml_ave=Avg(F('milk_today') / F('cows_milked'), output_field=models.FloatField())
    )['ml_ave'] if cow_numbers != 0 else 0
    if milking_average is None:
        milking_average = milking_average
    else:
        milking_average = Milk.objects.aggregate(
            ml_ave=Avg(F('milk_today') / F('cows_milked'), output_field=models.FloatField())
        )['ml_ave'] if cow_numbers != 0 else 0
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
    return render(request, 'mogoon/milk_table_create.html', context)


@login_required(login_url='login')
@never_cache
def milk_view_create(request):
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
def fertilizer_view_retrieve(request):
    data = Fertilizer.objects.all()
    fertilizer_applied = Fertilizer.objects.aggregate(Min('fertilizer_applied'))['fertilizer_applied__min']
    fertilizer_amt = Fertilizer.objects.aggregate(Sum('fertilizer_amt'))['fertilizer_amt__sum']
    fertilizer_labour_rate = Fertilizer.objects.aggregate(Sum('fertilizer_labour_rate'))['fertilizer_labour_rate__sum']
    fertilizer_labour = Fertilizer.objects.aggregate(Sum('fertilizer_labour'))['fertilizer_labour__sum']
    fertilizer_labour_cost = Fertilizer.objects.aggregate(Sum('fertilizer_labour_cost'))['fertilizer_labour_cost__sum']
    fertilizer_price = Fertilizer.objects.values('fertilizer_price').aggregate(Sum('fertilizer_price')).get(
        'fertilizer_price__sum', 0)
    fertilizer_cost = Fertilizer.objects.aggregate(
        tot_cost=Sum(
            Cast('fertilizer_amt', DecimalField()) * F('fertilizer_price'),
            output_field=DecimalField(),
        )
    ).get('tot_cost', Decimal('0'))
    fertilizer_total_cost = Fertilizer.objects.aggregate(
        total_cost=Sum(
            ExpressionWrapper(
                F('fertilizer_labour_cost') + (F('fertilizer_amt') * F('fertilizer_price')),
                output_field=models.FloatField()
            )
        )
    )['total_cost']

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
def fertilizer_view_fetch_details(request):
    form = UpdateFertilizerForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        # Assuming your form is based on the Fertilizer model
        fertilizer_instance = form.save(commit=False)
        fertilizer_amt = Fertilizer.objects.aggregate(Sum('fertilizer_amt'))['fertilizer_amt__sum']
        fertilizer_labour_rate = Fertilizer.objects.aggregate(Sum('fertilizer_labour_rate'))[
            'fertilizer_labour_rate__sum']
        fertilizer_labour = Fertilizer.objects.aggregate(Sum('fertilizer_labour'))['fertilizer_labour__sum']
        fertilizer_labour_cost = Fertilizer.objects.aggregate(Sum('fertilizer_labour_cost'))[
            'fertilizer_labour_cost__sum']
        if fertilizer_labour_cost is None:
            fertilizer_labour_cost = 0
        else:
            fertilizer_labour_cost = Fertilizer.objects.aggregate(Sum('fertilizer_labour_cost'))[
                'fertilizer_labour_cost__sum']
        fertilizer_price = Fertilizer.objects.values('fertilizer_price').aggregate(Sum('fertilizer_price')).get(
            'fertilizer_price__sum', 0)
        fertilizer_cost = Fertilizer.objects.aggregate(
            tot_cost=Sum(
                Cast('fertilizer_amt', DecimalField()) * F('fertilizer_price'),
                output_field=DecimalField(),
            )
        ).get('tot_cost', Decimal('0'))
        if fertilizer_cost is None:
            fertilizer_cost = 0
        else:
            fertilizer_cost = Fertilizer.objects.aggregate(
                tot_cost=Sum(
                    Cast('fertilizer_amt', DecimalField()) * F('fertilizer_price'),
                    output_field=DecimalField(),
                )
            ).get('tot_cost', Decimal('0'))
        fertilizer_total_cost = Fertilizer.objects.aggregate(
            total_cost=Sum(
                ExpressionWrapper(
                    F('fertilizer_labour_cost') + (F('fertilizer_amt') * F('fertilizer_price')),
                    output_field=models.FloatField()
                )
            )
        )['total_cost']
        if fertilizer_total_cost is None:
            fertilizer_total_cost = 0
        else:
            fertilizer_total_cost = Fertilizer.objects.aggregate(
                total_cost=Sum(
                    ExpressionWrapper(
                        F('fertilizer_labour_cost') + (F('fertilizer_amt') * F('fertilizer_price')),
                        output_field=models.FloatField()
                    )
                )
            )['total_cost']
        context = {
            "form": form,
            "fertilizer_amt": fertilizer_amt,
            "fertilizer_labour_rate": fertilizer_labour_rate,
            "fertilizer_labour": fertilizer_labour,
            "fertilizer_price": fertilizer_price,
            "fertilizer_labour_cost": fertilizer_labour_cost,
            "fertilizer_cost": fertilizer_cost,
            "fertilizer_total_cost": fertilizer_total_cost,

        }
        return render(request, 'mogoon/fertilizer_table_create.html', context)
    # If the form is not valid, or it's a GET request, render the form
    return render(request, 'mogoon/fertilizer_table_create.html', {"form": form})


@login_required(login_url='login')
@never_cache
def fertilizer_view_create(request):
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
##########################################################CRUD########################################################
@login_required(login_url='login')
def r_update(request, pk):
    # Use get_object_or_404 to handle the case where the Reports object is not found
    reports = get_object_or_404(Reports, id=pk)

    if request.method == 'POST':
        form = ReportsForm(request.POST, request.FILES, instance=reports)
        if form.is_valid():
            form.save()
            return redirect('/reports')

    else:
        form = ReportsForm(instance=reports)

    context = {
        'form': form,
        'ReportsForm': ReportsForm,  # Use the form class, not an instance
    }
    return render(request, 'Reports/update.html', context)


@login_required(login_url='login')
def r_delete(request, pk):
    # Use get_object_or_404 to handle the case where the Reports object is not found
    reports = get_object_or_404(Reports, id=pk)

    if request.method == 'POST':
        reports.delete()
        return redirect('/')

    context = {
        'item': reports,
    }
    return render(request, 'Reports/delete.html', context)


@login_required(login_url='login')
def employee_update(request, pk):
    data = Employee.objects.get(id=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/employee_list')

    else:
        form = EmployeeForm(instance=data)

    context = {
        'form': form, 'EmployeeForm': EmployeeForm,

    }
    return render(request, 'mogoon/employee_details_create.html', context)


@login_required(login_url='login')
def employee_edit(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            messages.success(request, 'Employee details are successfully updated.')
            return redirect('/employee-list')
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'Employee/update.html', {'form': form, 'employee': employee})


@login_required(login_url='login')
def employee_delete(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    if request.method == "POST":
        employee.delete()
        messages.success(request, 'Employee details are successfully deleted.')
        return redirect('/employee-list')
    context = {
        'item': employee,
    }
    return render(request, 'Employee/delete.html', context)


@login_required(login_url='login')
def update(request, pk):
    data = Green.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateGreenForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/green_table')

    else:
        form = UpdateGreenForm(instance=data)

    context = {
        'form': form, 'UpdateTaskForm': UpdateGreenForm,

    }
    return render(request, 'Green/update.html', context)


@login_required(login_url='login')
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
def f_update(request, pk):
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
def f_delete(request, pk):
    data = Fertilizer.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/fertilizer_table')

    context = {
        'item': data,
    }
    return render(request, 'Fertilizer/delete.html', context)


@login_required(login_url='login')
def k_update(request, pk):
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
def k_delete(request, pk):
    data = Kandojobs.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/kandojobs_table')

    context = {
        'item': data,
    }
    return render(request, 'Kandojobs/delete.html', context)


@login_required(login_url='login')
def m_update(request, pk):
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
def m_delete(request, pk):
    data = Milk.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/milk_table')

    context = {
        'item': data,
    }
    return render(request, 'Milk/delete.html', context)


@login_required(login_url='login')
def p_update(request, pk):
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
def p_delete(request, pk):
    data = Purple.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/purple_table')

    context = {
        'item': data,
    }
    return render(request, 'Purple/delete.html', context)


##################################################API FETCH URLS#######################################################
# API views
@api_view(['GET', 'POST'])
def reports_list_view(request):
    if request.method == 'GET':
        queryset = Reports.objects.all()
        serializer_class = ReportsSerializer(queryset, many=True)
        return Response(serializer_class.data)
    elif request.method == 'POST':
        serializer = ReportsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def reports_create_view(request):
    daily_report = request.POST.get('daily_report', False)
    visitors_name = request.POST.get('visitors_name', False)
    visitor_comments = request.POST.get('visitor_comments', False)
    farm_report = request.POST.get('farm_report', False)
    farm_requirements = request.POST.get('farm_requirements', False)
    farm_image = request.POST.get('farm_image', False)

    insert = Reports(
        daily_report=daily_report,
        visitors_name=visitors_name,
        visitor_comments=visitor_comments,
        farm_report=farm_report,
        farm_requirements=farm_requirements,
        farm_image=farm_image
    )
    insert.save()

    return Response(status=200)


@api_view(['GET', 'POST'])
def employee_list_view(request):
    if request.method == 'GET':
        queryset = Employee.objects.all()
        serializer_class = EmployeeSerializer(queryset, many=True)
        return Response(serializer_class.data)
    elif request.method == 'POST':
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def employee_create_view(request):
    date_employed = request.POST.get('date_employed', False)
    national_identity = request.POST.get('national_identity', False)
    name = request.POST.get('name', False)
    age = request.POST.get('age', False)
    gender = request.POST.get('gender', False)
    department = request.POST.get('department', False)
    position = request.POST.get('position', False)
    salary_total = request.POST.get('salary_total', False)

    insert = Employee(date_employed=date_employed, national_identity=national_identity, name=name, age=age,
                      gender=gender, department=department, position=position, salary_total=salary_total)
    insert.save()

    return Response(status=200)


@api_view(['GET'])
def green_list_view(request):
    queryset = Green.objects.all()
    serializer_class = GreenSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['POST'])
def green_create_view(request):
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

    return Response(status=200)


@api_view(['GET'])
def purple_list_view(request):
    queryset = Purple.objects.all()
    serializer_class = PurpleSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['POST'])
def purple_create_view(request):
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

    return Response(status=200)


@api_view(['GET'])
def kandojobs_list_create_view(request):
    queryset = Kandojobs.objects.all()
    serializer_class = KandojobsSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['POST'])
def kandojobs_create_view(request):
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
    return Response(status=200)


@api_view(['GET'])
def fertilizer_list_view(request):
    queryset = Fertilizer.objects.all()
    serializer_class = FertilizerSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['POST'])
def fertilizer_create_view(request):
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
    return Response(200)


@api_view(['GET'])
def milk_list_view(request):
    queryset = Milk.objects.all()
    serializer_class = MilkSerializer(queryset, many=True)
    return Response(serializer_class.data)


@api_view(['POST'])
def milk_create_view(request):
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
    return Response(200)

##################################################API FETCH URLS#######################################################


##################################################API CREATE URLS######################################################
