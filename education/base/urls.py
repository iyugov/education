from django.urls import path
from . import views

urlpatterns = [
    path('base/individuals/', views.individuals_list, name='individuals'),
    path('base/individual/new/', views.individual_new, name='individual_new'),
    path('base/individual/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('base/individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),
]
