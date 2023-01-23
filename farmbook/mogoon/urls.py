from django.urls import path
from . import views
from .views import *

# from django.conf.urls import patterns, url
urlpatterns = [

    path('', Home, name='home'),

    path('employee-e_details/', views.Employee_details, name='employee-details'),
    path('employee-e_list/', views.Employee_list, name='employee-list'),
    path('employee-e_update/', views.Employee_update, name='employee-update'),


    path('crop_table/', views.CropTable, name='mogoon-crop_table'),
    path('crop_table_update/', views.CropTableUpdate, name='mogoon-crop_table_update'),
    path('crop_create/', views.mogoonCropCreate, name='mogoon-crop_create'),

    path('purple_table/', views.CropPurpleTable, name='mogoon-purple'),
    path('purple_update/', views.CropPurpleTableUpdate, name='mogoon-purple_update'),
    path('purple_create/', views.CropPurpleCreate, name='mogoon-purple_create'),

    path('kandojobs_table/', views.KandojobsTable, name='mogoon-kandojobs_table'),
    path('kandojobs_table_update/', views.KandojobsTableUpdate, name='mogoon-kandojobs_table_update'),
    path('kandojobs_create/', views.mogoonKandojobsCreate, name='mogoon-kandojobs_create'),

    path('fertilizer_table/', views.FertilizerTable, name='mogoon-fertilizer_table'),
    path('fertilizer_table_update/', views.mogoonFertilizerTableUpdate,
         name='mogoon-fertilizer_table_update'),
    path('fertilizer_create/', views.mogoonFertilizerCreate, name='mogoon-fertilizer_create'),

    path('cashBreakdown_table/', views.CashBreakdownTable, name='mogoon-cashBreakdown'),
    path('cash_breakdown_create_table/', views.CashBreakdown_create, name='cash_breakdown_create'),
    path('cashBreakdown_create_update/', views.CashBreakdown_update, name='cash_breakdown_update'),
    path('cashBreakdown_update/', views.CashBreakdownUpdate, name='mogoon-cashBreakdown_update'),
    path('cashBreakdown_updateTotal/', views.CashBreakdownTotal, name='mogoon-cashBreakdown_total'),
    path('cashBreakdown_updateEdit/', views.CashBreakdownEdit, name='mogoon-cashBreakdown_edit'),
    path('cashBreakdown_create/', views.CashBreakdownCreate, name='mogoon-cashBreakdown_create'),


    path('milk_table/', views.MilkTable, name='mogoon-milk_table'),
    path('milk_table_update/', views.MilkTableUpdate, name='mogoon-milk_table_update'),
    path('milk_create/', views.mogoonMilkCreate, name='mogoon-milk_create'),

    path('employee-u_edit/<int:pk>/', views.Employee_edit, name='employee-edit'),
    path('employee-d_delete/<int:pk>/', views.Employee_delete, name='employee-delete'),

    path('update/<int:pk>/', views.update, name='Crop_data-update'),
    path('delete/<int:pk>/', views.delete, name='Crop_data-delete'),
    path('p_update/<int:pk>/', views.P_update, name='purple-update'),
    path('p_delete/<int:pk>/', views.P_delete, name='purple-delete'),
    path('f_update/<int:pk>/', views.F_update, name='fertilizer-update'),
    path('f_delete/<int:pk>/', views.F_delete, name='fertilizer-delete'),
    path('k_update/<int:pk>/', views.K_update, name='kandojobs-update'),
    path('k_delete/<int:pk>/', views.K_delete, name='kandojobs-delete'),
    path('m_update/<int:pk>/', views.M_update, name='milk-update'),
    path('m_delete/<int:pk>/', views.M_delete, name='milk-delete'),
    path('c_update/<int:pk>/', views.update, name='cashBreakdown-update'),
    path('c_delete/<int:pk>/', views.delete, name='cashBreakdown-delete'),
    path('R_update/<int:pk>/', views.R_update, name='cashBreakdown_r-update'),
    path('R_delete/<int:pk>/', views.R_delete, name='cashBreakdown_edit-delete'),

]

