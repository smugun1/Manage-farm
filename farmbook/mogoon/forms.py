from django import forms
from .models import Green, Fertilizer, Kandojobs, Milk, Employee, Purple


class TaskForms(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeDetailsForm(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Employee
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['date_employed', 'national_identity', 'name', 'age', 'gender', 'department', 'position', 'salary', 'total']
        label = {
            'date_employed': 'date_employed',
            'national_identity': 'National Identity',
            'name': 'Name',
            'age': 'Age',
            'gender': 'Gender',
            'department': 'Department',
            'position': 'Position',
            'salary': 'Salary',
            'total': 'Total'
        }


class TaskForm(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Green
        fields = '__all__'


class UpdatePurpleForm(forms.ModelForm):
    class Meta:
        model = Purple
        fields = '__all__'


class UpdateTaskForm(forms.ModelForm):
    class Meta:
        model = Green
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
