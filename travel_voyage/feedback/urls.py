from django.urls import path
from . import views

urlpatterns = [
    path('add_feedback/accommodation/<int:accommodation_id>/', views.add_feedback_accommodation, name='add_feedback_accommodation'),
    path('add_feedback/activity/<int:activity_id>/', views.add_feedback_activity, name='add_feedback_activity'),
    
]
