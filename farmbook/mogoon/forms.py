from django import forms
from .models import Green, Fertilizer, Kandojobs, Milk, Employee, Purple, Reports


class EmployeeForms(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Employee
        fields = '__all__'


class ReportsForm(forms.ModelForm):
    class Meta:
        model = Reports
        fields = '__all__'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = '__all__'


class UpdateGreenForm(forms.ModelForm):
    content = forms.CharField(label='SimKMN', widget=forms.TextInput(
        attrs={'placeholder': 'Add task here...'}))

    class Meta:
        model = Green
        fields = '__all__'


class UpdatePurpleForm(forms.ModelForm):
    class Meta:
        model = Purple
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
