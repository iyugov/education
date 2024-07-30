from django.urls import path
from . import views

urlpatterns = [
    path('individual/list/', views.individual_list, name='individual_list'),
    path('individual/new/', views.individual_new, name='individual_new'),
    path('individual/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),

    path('contact_info_type/list/', views.contact_info_type_list, name='contact_info_type_list'),
    path('contact_info_type/new/', views.contact_info_type_new, name='contact_info_type_new'),
    path('contact_info_type/<int:pk>/edit/', views.contact_info_type_edit, name='contact_info_type_edit'),
    path('contact_info_type/<int:pk>/delete/', views.ContactInfoTypeDelete.as_view(), name='contact_info_type_delete'),

]
