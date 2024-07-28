from django.urls import path
from . import views

urlpatterns = [
    path('base/class_group/list/', views.class_group_list, name='class_group_list'),
    path('base/class_group/new/', views.class_group_new, name='class_group_new'),
    path('base/class_group/<int:pk>/edit/', views.class_group_edit, name='class_group_edit'),
    path('base/class_group/<int:pk>/delete/', views.ClassGroupDelete.as_view(), name='class_group_delete'),
]
