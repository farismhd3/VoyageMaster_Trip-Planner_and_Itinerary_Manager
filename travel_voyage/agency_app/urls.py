from django.urls import path
from . import views

urlpatterns = [
    path('travel_agency_dashboard', views.travel_agency_dashboard, name='travel_agency_dashboard'),
    path('community/', views.agency_community, name='agency_community'),
    path('add_activity', views.add_activity, name='add_activity'),
    path('edit_activity/<int:activity_id>', views.edit_activity, name='edit_activity'),
    path('delete_activity/<int:activity_id>', views.delete_activity, name='delete_activity'),
    path('expense_page', views.agency_expense_tracker, name='expense_page'),
]
