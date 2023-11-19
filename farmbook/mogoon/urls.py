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
    path('', reports_view_retrieve, name='reports'),
    path('reports-update', reports_view_fetch_details, name='reports-update'),
    path('reports-create', reports_view_create, name='reports-create'),

    path('graph', graphs_view, name='graph'),

    path('employee-list/', views.employee_view_retrieve, name='employee-list'),
    path('employee-list_update/', views.employee_view_fetch_details, name='employee-list_update'),
    path('employees_create/', views.employee_view_create, name='mogoon-employees_create'),

    path('green_table/', views.green_view_retrieve, name='mogoon-green_table'),
    path('green_table_update/', views.green_view_fetch_details, name='mogoon-green_table_update'),
    path('green_create/', views.green_view_create, name='mogoon-green_create'),

    path('purple_table/', views.purple_view_retrieve, name='mogoon-purple'),
    path('purple_update/', views.purple_view_fetch_details, name='mogoon-purple_update'),
    path('purple_create/', views.purple_view_create, name='mogoon-purple_create'),

    path('kandojobs_table/', views.kandojobs_view_retrieve, name='mogoon-kandojobs_table'),
    path('kandojobs_table_update/', views.kandojobs_view_fetch_details, name='mogoon-kandojobs_table_update'),
    path('kandojobs_create/', views.kandojobs_view_create, name='mogoon-kandojobs_create'),

    path('fertilizer_table/', views.fertilizer_view_retrieve, name='mogoon-fertilizer_table'),
    path('fertilizer_table_update/', views.fertilizer_view_fetch_details,
         name='mogoon-fertilizer_table_update'),
    path('fertilizer_create/', views.fertilizer_view_create, name='mogoon-fertilizer_create'),

    path('milk_table/', views.milk_view_retrieve, name='mogoon-milk_table'),
    path('milk_table_update/', views.milk_view_fetch_details, name='mogoon-milk_table_update'),
    path('milk_create/', views.milk_view_create, name='mogoon-milk_create'),

    path('r_update/<str:pk>/', views.r_update, name='reports-edit'),
    path('r_delete/<str:pk>/', views.r_delete, name='reports-delete'),

    path('e_edit/<int:pk>/', views.employee_edit, name='employee-edit'),
    path('e_delete/<int:pk>/', views.employee_delete, name='employee-delete'),

    path('update/<int:pk>/', views.update, name='green_data-update'),
    path('delete/<int:pk>/', views.delete, name='green_data-delete'),
    path('p_update/<int:pk>/', views.p_update, name='purple-update'),
    path('p_delete/<int:pk>/', views.p_delete, name='purple-delete'),
    path('f_update/<int:pk>/', views.f_update, name='fertilizer-update'),
    path('f_delete/<int:pk>/', views.f_delete, name='fertilizer-delete'),
    path('k_update/<int:pk>/', views.k_update, name='kandojobs-update'),
    path('k_delete/<int:pk>/', views.k_delete, name='kandojobs-delete'),
    path('m_update/<int:pk>/', views.m_update, name='milk-update'),
    path('m_delete/<int:pk>/', views.m_delete, name='milk-delete'),

    path('employee_api/', views.employee_list_view),
    path('green_api/', views.green_list_view),
    path('purple_api/', views.purple_list_view),
    path('kandojobs_api/', views.kandojobs_list_create_view),
    path('fertilizer_api/', views.fertilizer_list_view),
    path('milk_api/', views.milk_list_view),

    path('employee_create_api/', views.employee_create_view),
    path('green_create_api/', views.green_create_view),
    path('purple_create_api/', views.purple_create_view),
    path('kandojobs_create_api/', views.kandojobs_create_view),
    path('fertilizer_create_api/', views.fertilizer_create_view),
    path('milk_create_api/', views.milk_create_view),

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
