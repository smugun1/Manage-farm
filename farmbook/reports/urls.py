# from django.urls import path
#
# from . import views
# # from .apiViews import ReportsListCreateAPIView, ReportsRetrtieveUpdateDestroyAPIView,
#
# from .views import *
# from ..mogoon.views import reports_view_retrieve, reports_view_fetch_details, reports_view_create, graphs_view
#
# # from django.conf.urls import patterns, url
#
#
# urlpatterns = [
#     path('', reports_view_retrieve, name='reports-retrieve'),
#     path('reports-details', reports_view_fetch_details, name='reports-details'),
#     path('reports-create', reports_view_create, name='reports-create'),
#
#     path('graph', graphs_view, name='graph'),
#
#
#
#     path('reports_update/<int:pk>/', views.reports_view_update, name='reports-update'),
#     path('reports_delete/<int:pk>/', views.reports_view_delete, name='reports-delete'),
#
#
#
#     path('reports_api/', views.reports_list_view),
#
#
#     path('reports_create_api/', views.reports_create_view),
#
#
#     path('generics-reports/', ReportsListCreateAPIView.as_view()),
#     path('generics-reports/<int:pk>/', ReportsRetrtieveUpdateDestroyAPIView.as_view()),
#
#
# ]
