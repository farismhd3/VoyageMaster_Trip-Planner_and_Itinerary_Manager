from django.urls import path
from .views import *

urlpatterns = [
    path('add_notification', add_notification, name='add_notification'),
    path('notifications', notification_list, name='notification_list'),
    path('notifications/mark_as_read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
   
    path('agency/notifications/mark_as_read/<int:notification_id>/', mark_agency_notification_as_read, name='mark_agency_notification_as_read'),
]
