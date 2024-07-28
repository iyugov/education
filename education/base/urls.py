from django.urls import path
from . import views

urlpatterns = [
    path('base/individual/list/', views.individual_list, name='individual_list'),
    path('base/individual/new/', views.individual_new, name='individual_new'),
    path('base/individual/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('base/individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),
]
