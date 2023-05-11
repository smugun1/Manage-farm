from django.urls import path

from . import views
from .apiViews import EmployeeListCreateAPIView, EmployeeRetrtieveUpdateDestroyAPIView, ReportsListCreateAPIView, \
    ReportsRetrtieveUpdateDestroyAPIView, GreenListCreateAPIView, GreenRetrtieveUpdateDestroyAPIView, \
    PurpleListCreateAPIView, PurpleRetrtieveUpdateDestroyAPIView, KandojobsListCreateAPIView, \
    KandojobsRetrtieveUpdateDestroyAPIView, MilkListCreateAPIView, MilkRetrtieveUpdateDestroyAPIView, \
    FertilizerListCreateAPIView, FertilizerRetrtieveUpdateDestroyAPIView
from .views import *

# from django.conf.urls import patterns, url


urlpatterns = [
    path('', ReportsViewRetrieve, name='reports'),
    path('reports-update', ReportsViewUpdate, name='reports-update'),
    path('reports-create', ReportsViewCreate, name='reports-create'),

    path('employee-list/', views.EmployeeViewRetrieve, name='employee-list'),
    path('employee-list_update/', views.EmployeeViewUpdate, name='employee-list_update'),
    path('employees_create/', views.EmployeeViewCreate, name='mogoon-employees_create'),

    path('green_table/', views.GreenViewRetrieve, name='mogoon-green_table'),
    path('green_table_update/', views.GreenViewUpdate, name='mogoon-green_table_update'),
    path('green_create/', views.GreenViewCreate, name='mogoon-green_create'),

    path('purple_table/', views.PurpleViewRetrieve, name='mogoon-purple'),
    path('purple_update/', views.PurpleViewUpdate, name='mogoon-purple_update'),
    path('purple_create/', views.PurpleViewCreate, name='mogoon-purple_create'),

    path('kandojobs_table/', views.KandojobsViewRetrieve, name='mogoon-kandojobs_table'),
    path('kandojobs_table_update/', views.KandojobsViewUpdate, name='mogoon-kandojobs_table_update'),
    path('kandojobs_create/', views.KandojobsViewCreate, name='mogoon-kandojobs_create'),

    path('fertilizer_table/', views.FertilizerViewRetrieve, name='mogoon-fertilizer_table'),
    path('fertilizer_table_update/', views.FertilizerViewUpdate,
         name='mogoon-fertilizer_table_update'),
    path('fertilizer_create/', views.FertilizerViewCreate, name='mogoon-fertilizer_create'),

    path('milk_table/', views.MilkViewRetrieve, name='mogoon-milk_table'),
    path('milk_table_update/', views.MilkViewUpdate, name='mogoon-milk_table_update'),
    path('milk_create/', views.MilkViewCreate, name='mogoon-milk_create'),

    path('r_update/<str:pk>/', views.R_update, name='reports-edit'),
    path('r_delete/<str:pk>/', views.R_delete, name='reports-delete'),

    path('e_edit/<int:pk>/', views.Employee_edit, name='employee-edit'),
    path('e_delete/<int:pk>/', views.Employee_delete, name='employee-delete'),

    path('update/<int:pk>/', views.update, name='green_data-update'),
    path('delete/<int:pk>/', views.delete, name='green_data-delete'),
    path('p_update/<int:pk>/', views.P_update, name='purple-update'),
    path('p_delete/<int:pk>/', views.P_delete, name='purple-delete'),
    path('f_update/<int:pk>/', views.F_update, name='fertilizer-update'),
    path('f_delete/<int:pk>/', views.F_delete, name='fertilizer-delete'),
    path('k_update/<int:pk>/', views.K_update, name='kandojobs-update'),
    path('k_delete/<int:pk>/', views.K_delete, name='kandojobs-delete'),
    path('m_update/<int:pk>/', views.M_update, name='milk-update'),
    path('m_delete/<int:pk>/', views.M_delete, name='milk-delete'),

    path('employee_api/', views.EmployeeListView),
    path('green_api/', views.GreenListView),
    path('purple_api/', views.PurpleListView),
    path('kandojobs_api/', views.KandojobsListCreateView),
    path('fertilizer_api/', views.FertilizerListView),
    path('milk_api/', views.MilkListView),

    path('employee_create_api/', views.EmployeeCreateView),
    path('green_create_api/', views.GreenCreateView),
    path('purple_create_api/', views.PurpleCreateView),
    path('kandojobs_create_api/', views.KandojobsCreateView),
    path('fertilizer_create_api/', views.FertilizerCreateView),
    path('milk_create_api/', views.MilkCreateView),

    path('generics-reports/', ReportsListCreateAPIView.as_view()),
    path('generics-reports/<int:pk>/', ReportsRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-employee/', EmployeeListCreateAPIView.as_view()),
    path('generics-employee/<int:pk>/', EmployeeRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-green/', GreenListCreateAPIView.as_view()),
    path('generics-green/<int:pk>/', GreenRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-purple/', PurpleListCreateAPIView.as_view()),
    path('generics-purple/<int:pk>/', PurpleRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-kandojobs/', KandojobsListCreateAPIView.as_view()),
    path('generics-kandojobs/<int:pk>/', KandojobsRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-milk/', MilkListCreateAPIView.as_view()),
    path('generics-milk/<int:pk>/', MilkRetrtieveUpdateDestroyAPIView.as_view()),
    path('generics-fertilizer/', FertilizerListCreateAPIView.as_view()),
    path('generics-fertilizer/<int:pk>/', FertilizerRetrtieveUpdateDestroyAPIView.as_view()),

]
