from django.urls import path
from . import views

app_name = 'community'

urlpatterns = [
    path('', views.discussion_list, name='discussion_list'),
    path('create/', views.create_discussion, name='create_discussion'),
    path('discussion/<int:pk>/', views.discussion_detail, name='discussion_detail'),
    path('discussion/<int:discussion_pk>/create-post/', views.create_post, name='create_post'),
    # path('discussion_detail/<int:pk>', views.discussion_detail, name='discussion_detail'),
    path('post/<int:post_pk>/like/', views.like_post, name='like_post'),
    path('post/<int:post_pk>/comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.toggle_like, name='toggle_like'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('discussion/<int:discussion_pk>/delete/', views.delete_discussion, name='delete_discussion'),

] 