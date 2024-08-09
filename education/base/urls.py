from django.urls import path
from . import views

from django.views.generic import TemplateView

urlpatterns = [
    path('individual/list/', views.individual_list, name='individual_list'),
    path('individual/new/', views.individual_item, name='individual_new'),
    path('individual/<int:pk>/edit/', views.individual_item, name='individual_edit'),
    path('individual/<int:pk>/delete/', views.IndividualDelete.as_view(), name='individual_delete'),
    path('individual/upload_csv/', views.individual_upload_csv, name='individual_upload_csv'),
    path('individual/upload_csv_result/', TemplateView.as_view(template_name="entities/individual/upload_csv_result.html"), name='individual_upload_csv_result'),

    path('contact_info_type/list/', views.contact_info_type_list, name='contact_info_type_list'),
    path('contact_info_type/new/', views.contact_info_type_item, name='contact_info_type_new'),
    path('contact_info_type/<int:pk>/edit/', views.contact_info_type_item, name='contact_info_type_edit'),
    path('contact_info_type/<int:pk>/delete/', views.ContactInfoTypeDelete.as_view(), name='contact_info_type_delete'),

    path('student/list/', views.student_list, name='student_list'),
    path('student/new/', views.student_item, name='student_new'),
    path('student/<int:pk>/edit/', views.student_item, name='student_edit'),
    path('student/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),

    path('class_group/list/', views.class_group_list, name='class_group_list'),
    path('class_group/new/', views.class_group_item, name='class_group_new'),
    path('class_group/<int:pk>/edit/', views.class_group_item, name='class_group_edit'),
    path('class_group/<int:pk>/delete/', views.ClassGroupDelete.as_view(), name='class_group_delete'),

    path('class_group_enrollment/list/', views.class_group_enrollment_list, name='class_group_enrollment_list'),
    path('class_group_enrollment/new/', views.class_group_enrollment_item, name='class_group_enrollment_new'),
    path('class_group_enrollment/<int:pk>/edit/', views.class_group_enrollment_item,
         name='class_group_enrollment_edit'),
    path('class_group_enrollment/<int:pk>/delete/', views.ClassGroupEnrollmentDelete.as_view(),
         name='class_group_enrollment_delete'),

    path('pass_tag/list/', views.pass_tag_list, name='pass_tag_list'),
    path('pass_tag/new/', views.pass_tag_item, name='pass_tag_new'),
    path('pass_tag/<int:pk>/edit/', views.pass_tag_item, name='pass_tag_edit'),
    path('pass_tag/<int:pk>/delete/', views.PassTagDelete.as_view(), name='pass_tag_delete'),
    path('pass_tag/upload_csv/', views.pass_tag_upload_csv, name='pass_tag_upload_csv'),
    path('pass_tag/upload_csv_result/', TemplateView.as_view(template_name="entities/pass_tag/upload_csv_result.html"),
         name='pass_tag_upload_csv_result'),

    path('pass_tag_request/list/', views.pass_tag_request_list, name='pass_tag_request_list'),
    path('pass_tag_request/new/', views.pass_tag_request_item, name='pass_tag_request_new'),
    path('pass_tag_request/<int:pk>/edit/', views.pass_tag_request_item, name='pass_tag_request_edit'),
    path('pass_tag_request/<int:pk>/delete/', views.PassTagRequestDelete.as_view(), name='pass_tag_request_delete'),

]
