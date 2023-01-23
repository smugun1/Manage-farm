from django import forms
from .models import Crop, Fertilizer, Kandojobs, Milk, CashBreakdown, Employee


class TaskForms(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['national_identity', 'name', 'age', 'gender', 'department', 'position', 'salary']
        label = {
            'national_identity': 'National Identity',
            'name': 'Name',
            'age': 'Age',
            'gender': 'Gender',
            'department': 'Department',
            'position': 'Position',
            'salary': 'Salary'
        }


class TaskForm(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Crop
        fields = '__all__'


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = '__all__'


class UpdateFertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = '__all__'


class UpdateKandojobsForm(forms.ModelForm):
    class Meta:
        model = Kandojobs
        fields = '__all__'


class UpdateMilkForm(forms.ModelForm):
    class Meta:
        model = Milk
        fields = '__all__'


class UpdateCashBreakdownForm(forms.ModelForm):
    class Meta:
        model = CashBreakdown
        fields = '__all__'


class CashBreakdownForm(forms.ModelForm):
    class Meta:
        model = CashBreakdown
        fields = '__all__'
