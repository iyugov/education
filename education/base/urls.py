from django.urls import path
from . import views

urlpatterns = [
    path('base/individual/list/', views.individual_list, name='individual_list'),
    path('base/individual/new/', views.individual_new, name='individual_new'),
    path('base/individual/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('base/individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),

    path('base/contact_info_type/list/', views.contact_info_type_list, name='contact_info_type_list'),
    path('base/contact_info_type/new/', views.contact_info_type_new, name='contact_info_type_new'),
    path('base/contact_info_type/<int:pk>/edit/', views.contact_info_type_edit, name='contact_info_type_edit'),
    path('base/contact_info_type/<int:pk>/delete/', views.ContactInfoTypeDelete.as_view(), name='contact_info_type_delete'),
]
