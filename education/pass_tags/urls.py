from django.urls import path
from . import views

urlpatterns = [

    path('pass_tag/list/', views.pass_tag_list, name='pass_tag_list'),
    path('pass_tag/new/', views.pass_tag_new, name='pass_tag_new'),
    path('pass_tag/<int:pk>/edit/', views.pass_tag_edit, name='pass_tag_edit'),
    path('pass_tag/<int:pk>/delete/', views.PassTagDelete.as_view(), name='pass_tag_delete'),
    
    path('pass_tag_request/list/', views.pass_tag_request_list, name='pass_tag_request_list'),
    path('pass_tag_request/new/', views.pass_tag_request_new, name='pass_tag_request_new'),
    path('pass_tag_request/<int:pk>/edit/', views.pass_tag_request_edit, name='pass_tag_request_edit'),
    path('pass_tag_request/<int:pk>/delete/', views.PassTagRequestDelete.as_view(), name='pass_tag_request_delete'),
]
