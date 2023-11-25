# from django.db import models
#
#
# # Create your models here.
# class Reports(models.Model):
#     daily_report = models.CharField(max_length=2000)
#     visitors_name = models.CharField(max_length=100)
#     visitor_comments = models.CharField(max_length=2000)
#     farm_report = models.CharField(max_length=2000)
#     farm_requirements = models.CharField(max_length=200)
#     time_stamp = models.DateTimeField(auto_now_add=True)
#     farm_image = models.ImageField(null=True, blank=True, upload_to="images/")
#
#     def __str__(self):
#         return self.daily_report
#
#     # @property
#     # def imageURL(self):
#     #     try:
#     #         url = self.farm_image.url
#     #     except:
#     #         url = ''
#     #     return url
#
#     class Meta:
#         ordering = ('-time_stamp',)
#
#
# class Employee(models.Model):
#     GENDER_CHOICES = (
#         ('M', 'Male'),
#         ('F', 'Female'),
#     )
#     DEPARTMENT_CHOICES = (
#         ('Administration', 'Adm'), ('Security', 'Sec'), ('Management', 'Mgt'), ('Field', 'Fld'),
#         ('Office', 'Off'), ('Stores', 'Str'), ('Other', 'Other'),
#     )
#
#     POSITION_CHOICES = (
#         ('Guard', 'Grd'), ('Plucker', 'Plk'), ('Dairy', 'Dairy'), ('Kando', 'Kando'), ('Cook', 'Ck'),
#         ('Office Messanger', 'Off Mgr'), ('Store', 'Str'), ('Director', 'Dir'), ('Estate Worker', 'Est Wkr'),
#         ('Assistant Manager', 'Asst Mgr'), ('Accountant', 'Acct'), ('Supervisor', 'Sup'), ('Clerk', 'Clk'),
#     )
#
#     date_employed = models.DateTimeField(auto_now_add=False, blank=False)
#     national_identity = models.CharField(max_length=100)
#     name = models.CharField(max_length=100)
#     age = models.IntegerField()
#     gender = models.CharField(max_length=1, choices=GENDER_CHOICES, )
#     department = models.CharField(max_length=100, choices=DEPARTMENT_CHOICES, )
#     position = models.CharField(max_length=100, choices=POSITION_CHOICES, )
#     salary_total = models.IntegerField()
#
#     def __str__(self):
#         return f'{self.date_employed}-{self.national_identity}-{self.name}-{self.age}{self.gender}-{self.department}' \
#                f'{self.position}-{self.salary_total}'
