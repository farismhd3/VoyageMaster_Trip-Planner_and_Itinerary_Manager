from django.urls import path
from . import views

urlpatterns = [
    path('add_accommodation/', views.add_accommodation, name='add_accommodation'),
    path('edit_accommodation/<int:accommodation_id>/', views.edit_accommodation, name='edit_accommodation'),
    path('delete_accommodation/<int:accommodation_id>/', views.delete_accommodation, name='delete_accommodation'),
    # path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
]
