# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
# from django.views.decorators.cache import never_cache
#
#
# # Create your views here.
# # Create your views here.
# @login_required(login_url='login')
# @never_cache
# def reports_view_retrieve(request):
#     reports = Reports.objects.all()
#     form = ReportsForm()
#
#     context = {
#         "name": "Reports Page",  # Remove unnecessary curly braces
#         'reports': reports,
#         "ReportsForm": form,  # Pass the form instance
#     }
#     return render(request, 'mogoon/view_reports.html', context)
#
#
# @login_required(login_url='login')
# @never_cache
# def reports_view_fetch_details(request):
#     if request.method == "POST":
#         form = ReportsForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Assuming your form has fields like daily_report, visitors_name, etc.
#             daily_report = form.cleaned_data['daily_report']
#             visitors_name = form.cleaned_data['visitors_name']
#             visitor_comments = form.cleaned_data['visitor_comments']
#             farm_report = form.cleaned_data['farm_report']
#             farm_requirements = form.cleaned_data['farm_requirements']
#             farm_image = form.cleaned_data['farm_image']
#
#             context = {
#                 "daily_report": daily_report,
#                 "visitors_name": visitors_name,
#                 "visitor_comments": visitor_comments,
#                 "farm_report": farm_report,
#                 "farm_requirements": farm_requirements,
#                 "farm_image": farm_image,
#             }
#             return render(request, 'mogoon/reports_create.html', context)
#     else:
#         form = ReportsForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'mogoon/reports_create.html', context)
#
#
# @login_required(login_url='login')
# @never_cache
# def reports_view_create(request):
#     if request.method == 'POST':
#         form = ReportsForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Access cleaned data, including the file, from the form
#             daily_report = form.cleaned_data['daily_report']
#             visitors_name = form.cleaned_data['visitors_name']
#             visitor_comments = form.cleaned_data['visitor_comments']
#             farm_report = form.cleaned_data['farm_report']
#             farm_requirements = form.cleaned_data['farm_requirements']
#             farm_image = form.cleaned_data['farm_image']
#
#             # Create and save the Reports object
#             insert = Reports(
#                 daily_report=daily_report,
#                 visitors_name=visitors_name,
#                 visitor_comments=visitor_comments,
#                 farm_report=farm_report,
#                 farm_requirements=farm_requirements,
#                 farm_image=farm_image
#             )
#             insert.save()
#
#             return redirect('/')
#     else:
#         form = ReportsForm()
#
#     return render(request, 'mogoon/view_reports.html', {'form': form})
#
#
# def graphs_view(request):
#     # Retrieve data from various models
#     employees_data = Employee.objects.all()
#     green_data = Green.objects.all()
#     purple_data = Purple.objects.all()
#     pruning_data = Pruning.objects.all()
#     weeding_data = Pruning.objects.all()
#     fertilizer_data = Fertilizer.objects.all()
#     milk_data = Milk.objects.all()
#     vetcosts_data = VetCosts.objects.all()
#
#     # Use specific forms for each model
#     employee_form = EmployeeForm(request.POST or None)
#     green_form = UpdateGreenForm(request.POST or None)
#     purple_form = UpdatePurpleForm(request.POST or None)
#     pruning_form = PruningForm(request.POST or None)
#     weeding_form = WeedingForm(request.POST or None)
#     fertilizer_form = UpdateFertilizerForm(request.POST or None)
#     milk_form = UpdateMilkForm(request.POST or None)
#     vetcosts_form = VetCostsForm(request.POST or None)
#
#     # Combine data and forms into a dictionary
#     data_and_forms = {
#         'Employees': {'data': employees_data, 'form': employee_form},
#         'Green': {'data': green_data, 'form': green_form},
#         'Purple': {'data': purple_data, 'form': purple_form},
#         'pruning': {'data': pruning_data, 'form': pruning_form},
#         'weeding': {'data': weeding_data, 'form': weeding_form},
#         'Fertilizer': {'data': fertilizer_data, 'form': fertilizer_form},
#         'Milk': {'data': milk_data, 'form': milk_form},
#         'VetCosts': {'data': vetcosts_data, 'form': vetcosts_form},
#     }
#
#     if request.method == 'POST':
#         # Determine the form submitted and handle it accordingly
#         form_name = request.POST.get('form_name')
#         if form_name in data_and_forms:
#             current_form = data_and_forms[form_name]['form']
#             if current_form.is_valid():
#                 current_form.save()
#
#     context = {
#         'name': 'This is the graphs dashboard',
#         'data_and_forms': data_and_forms,
#     }
#
#     return render(request, 'mogoon/graphs.html', context)