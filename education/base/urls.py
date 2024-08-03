from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('individual/list/', views.individual_list, name='individual_list'),
    path('individual/new/', views.individual_new, name='individual_new'),
    path('individual/<int:pk>/edit/', views.individual_edit, name='individual_edit'),
    path('individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),
    path('individual/upload_csv/', views.individual_upload_csv, name='individual_upload_csv'),
    path('individual/upload_csv_result/', TemplateView.as_view(template_name="entities/individual/upload_csv_result.html"), name='individual_upload_csv_result'),

    path('contact_info_type/list/', views.contact_info_type_list, name='contact_info_type_list'),
    path('contact_info_type/new/', views.contact_info_type_new, name='contact_info_type_new'),
    path('contact_info_type/<int:pk>/edit/', views.contact_info_type_edit, name='contact_info_type_edit'),
    path('contact_info_type/<int:pk>/delete/', views.ContactInfoTypeDelete.as_view(), name='contact_info_type_delete'),

]
