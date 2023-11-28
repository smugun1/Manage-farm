from django.urls import path

from . import views
from .apiViews import EmployeeListCreateAPIView, EmployeeRetrieveUpdateDestroyAPIView, ReportsListCreateAPIView, \
    ReportsRetrieveUpdateDestroyAPIView, GreenListCreateAPIView, GreenRetrieveUpdateDestroyAPIView, \
    PurpleListCreateAPIView, PurpleRetrieveUpdateDestroyAPIView, \
    FertilizerListCreateAPIView, FertilizerRetrieveUpdateDestroyAPIView, WeedingListCreateAPIView, \
    PruningListCreateAPIView, PruningRetrieveUpdateDestroyAPIView, \
    WeedingRetrieveUpdateDestroyAPIView, MilkListCreateAPIView, \
    MilkRetrieveUpdateDestroyAPIView, VetCostsListCreateAPIView, VetCostsRetrieveUpdateDestroyAPIView
from .views import *

# from django.conf.urls import patterns, url


urlpatterns = [
    path('', reports_view_retrieve, name='reports-retrieve'),
    path('reports-details/', reports_view_fetch_details, name='reports-details'),
    path('reports-create/', reports_view_create, name='reports-create'),

    path('graph/', graphs_view, name='graph'),

    path('employee-retrieve/', views.employee_view_retrieve, name='employee-retrieve'),
    path('employee-details/', views.employee_view_fetch_details, name='employee-details'),
    path('employees-create/', views.employee_view_create, name='employees-create'),

    path('green-retrieve/', views.green_view_retrieve, name='green-retrieve'),
    path('green-details/', views.green_view_fetch_details, name='green-details'),
    path('green-create/', views.green_view_create, name='green-create'),

    path('purple-retrieve/', views.purple_view_retrieve, name='purple-retrieve'),
    path('purple-details/', views.purple_view_fetch_details, name='purple-details'),
    path('purple-create/', views.purple_view_create, name='purple-create'),

    path('pruning-retrieve/', views.pruning_view_retrieve, name='pruning-retrieve'),
    path('pruning-details/', views.pruning_view_fetch_details, name='pruning-details'),
    path('pruning-create/', views.pruning_view_create, name='pruning-create'),

    path('weeding-retrieve/', views.weeding_view_retrieve, name='weeding-retrieve'),
    path('weeding-details/', views.weeding_view_fetch_details, name='weeding-details'),
    path('weeding-create/', views.weeding_view_create, name='weeding-create'),

    path('fertilizer-retrieve/', views.fertilizer_view_retrieve, name='fertilizer-retrieve'),
    path('fertilizer-details/', views.fertilizer_view_fetch_details,
         name='fertilizer-details'),
    path('fertilizer-create/', views.fertilizer_view_create, name='fertilizer-create'),

    path('milk-retrieve/', views.milk_view_retrieve, name='milk-retrieve'),
    path('milk-details/', views.milk_view_fetch_details, name='milk-details'),
    path('milk-create/', views.milk_view_create, name='milk-create'),

    path('vetcosts-retrieve/', views.vetcosts_view_retrieve, name='vetcosts-retrieve'),
    path('vetcosts-details/', views.vetcosts_view_fetch_details, name='vetcosts-details'),
    path('vetcosts-create/', views.vetcosts_view_create, name='vetcosts-create'),

    path('reports-update/<int:pk>/', views.reports_view_update, name='reports-update'),
    path('reports-delete/<int:pk>/', views.reports_view_delete, name='reports-delete'),

    path('employee-update/<int:pk>/', views.employee_view_update, name='employee-update'),
    path('employee-delete/<int:pk>/', views.employee_view_delete, name='employee-delete'),

    path('green-update/<int:pk>/', views.update, name='green-update'),
    path('green-delete/<int:pk>/', views.delete, name='green-delete'),

    path('purple-update/<int:pk>/', views.purple_view_update, name='purple-update'),
    path('purple-delete/<int:pk>/', views.purple_view_delete, name='purple-delete'),

    path('fertilizer-update/<int:pk>/', views.fertilizer_view_update, name='fertilizer-update'),
    path('fertilizer-delete/<int:pk>/', views.fertilizer_view_delete, name='fertilizer-delete'),

    path('pruning-update/<int:pk>/', views.pruning_view_update, name='pruning-update'),
    path('pruning-delete/<int:pk>/', views.pruning_view_delete, name='pruning-delete'),

    path('weeding-update/<int:pk>/', views.weeding_view_update, name='weeding-update'),
    path('weeding-delete/<int:pk>/', views.weeding_view_delete, name='weeding-delete'),

    path('milk-update/<int:pk>/', views.milk_view_update, name='milk-update'),
    path('milk-delete/<int:pk>/', views.milk_view_delete, name='milk-delete'),

    path('vetcosts-update/<int:pk>/', views.vetcosts_view_update, name='vetcosts-update'),
    path('vetcosts-delete/<int:pk>/', views.vetcosts_view_delete, name='vetcosts-delete'),

    path('reports_api/', views.reports_list_view),
    path('employee_api/', views.employee_list_view),
    path('green_api/', views.green_list_view),
    path('purple_api/', views.purple_list_view),
    path('pruning_api/', views.pruning_list_create_view),
    path('weeding_api/', views.weeding_list_create_view),
    path('fertilizer_api/', views.fertilizer_list_view),
    path('milk_api/', views.milk_list_view),
    path('vetcosts_api/', views.vetcosts_list_view),

    path('reports_create_api/', views.reports_create_view),
    path('employee_create_api/', views.employee_create_view),
    path('green_create_api/', views.green_create_view),
    path('purple_create_api/', views.purple_create_view),
    path('pruning_create_api/', views.pruning_create_view),
    path('weeding_create_api/', views.weeding_create_view),
    path('fertilizer_create_api/', views.fertilizer_create_view),
    path('milk_create_api/', views.milk_create_view),
    path('vetcosts_create_api/', views.vetcosts_create_view),

    path('generics-reports/', ReportsListCreateAPIView.as_view()),
    path('generics-reports/<int:pk>/', ReportsRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-employee/', EmployeeListCreateAPIView.as_view()),
    path('generics-employee/<int:pk>/', EmployeeRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-green/', GreenListCreateAPIView.as_view()),
    path('generics-green/<int:pk>/', GreenRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-purple/', PurpleListCreateAPIView.as_view()),
    path('generics-purple/<int:pk>/', PurpleRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-pruning/', PruningListCreateAPIView.as_view()),
    path('generics-pruning/<int:pk>/', PruningRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-weeding/', WeedingListCreateAPIView.as_view()),
    path('generics-weeding/<int:pk>/', WeedingRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-milk/', MilkListCreateAPIView.as_view()),
    path('generics-milk/<int:pk>/', MilkRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-vetcosts/', VetCostsListCreateAPIView.as_view()),
    path('generics-vetcosts/<int:pk>/', VetCostsRetrieveUpdateDestroyAPIView.as_view()),
    path('generics-fertilizer/', FertilizerListCreateAPIView.as_view()),
    path('generics-fertilizer/<int:pk>/', FertilizerRetrieveUpdateDestroyAPIView.as_view()),

]