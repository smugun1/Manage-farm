def Employee_list(request):
    employee_list = Employee.objects.all()
    date_employed = models.DateTimeField()
    national_identity = models.IntegerField()
    name = models.model.CharField()
    age = models.models.IntegerField()
    gender = models.models.model.CharField()
    department = models.models.model.CharField()
    position = models.models.model.CharField()
    salary = Employee.objects.aggregate(sal_count=Count('salary'))
    total = Employee.objects.aggregate(sal_total=Sum('salary'))
    return render(request, 'mogoon/employee_list.html', {'employee_list': employee_list})


@never_cache
def Employee_update(request):
    employee_list = Employee.objects.all()
    date_employed = models.DateTimeField()
    salary = Employee.objects.aggregate(sal_count=Count('salary'))
    total = Employee.objects.aggregate(sal_total=Sum('salary'))
    form = EmployeeDetailsForm(instance=employee)
    if salary.get('sal_count') is None:
        salary['sal_count'] = 0
    else:
        salary = Employee.objects.aggregate(sal_count=Count('salary'))

    if total.get('sal_total') is None:
        total['sal_total'] = 0
    else:
        total = Employee.objects.aggregate(sal_total=Sum('salary'))

    if request.method == 'POST':
        form = EmployeeDetailsForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee-details', pk=pk)
    context = {'form': form}
    return render(request, 'mogoon/employee_details_update.html', context)



def Employee_create(request):
    if request.method == "POST":
        date_employed = request.POST['date_employed']
        national_identity = request.POST['national_identity']
        name = request.POST['name']
        age = request.POST['age']
        gender = request.POST['gender']
        department = request.POST['department']
        position = request.POST['position']
        salary = request.POST['salary']
        total = request.POST['total']

        insert = Employee(date_employed=date_employed, national_identity=national_identity, name=name, age=age,
                          gender=gender, department=department, position=position, salary=salary, total=total)
        insert.save()
        return redirect('employee-list')

    return render(request, 'mogoon/employee_create.html')
