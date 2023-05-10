# to be removed when app is completed.
# Used for rearranging code and has no connection to the app.

def PurpleView(request):
    data = Purple.objects.all()
    plucking_date = purple._meta.get_field('plucking_date').verbose_name

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
    return render(request, 'mogoon/purple_table.html', context)


@login_required(login_url='login')
@login_required
def R_update(request, pk):
    data = Reports.objects.get(id=pk)
    if request.method == 'POST':
        form = ReportsForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('/reports')

    else:
        form = ReportsForm(instance=data)

    context = {
        'form': form, 'ReportsForm': ReportsForm,

    }
    return render(request, 'Reports/update.html', context)


@login_required(login_url='login')
@login_required
def R_delete(request, pk):
    data = Reports.objects.get(id=pk)
    if request.method == 'POST':
        data.delete()
        return redirect('/reports')

    context = {
        'item': data,
    }
    return render(request, 'Reports/delete.html', context)

