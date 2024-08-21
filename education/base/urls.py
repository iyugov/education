from django.urls import path

from .entities.catalogs.student import views as student_views
from .entities.catalogs.class_group import views as class_group_views
from .entities.catalogs.pass_tag import views as pass_tag_views
from .entities.catalogs.individual import views as individual_views
from .entities.catalogs.contact_info_type import views as contact_info_type_views
from .entities.catalogs.employee import views as employee_views
from .entities.catalogs.position import views as position_views

from .entities.documents.pass_tag_request import views as pass_tag_request_views
from .entities.documents.class_group_enrollment import views as class_group_enrollment_views

from django.views.generic import TemplateView

from .generic_views import generic_view

urlpatterns = [

    path('', generic_view, name=''),

    path('individual/list/', individual_views.individual_list, name='individual_list'),
    path('individual/new/', individual_views.individual_item, name='individual_new'),
    path('individual/<int:pk>/edit/', individual_views.individual_item, name='individual_edit'),
    path('individual/<int:pk>/delete/', individual_views.IndividualDelete.as_view(), name='individual_delete'),
    path('individual/upload_csv/', individual_views.individual_upload_csv, name='individual_upload_csv'),
    path('individual/upload_csv_result/', TemplateView.as_view(template_name="entities/individual/upload_csv_result.html"), name='individual_upload_csv_result'),

    path('contact_info_type/list/', contact_info_type_views.contact_info_type_list, name='contact_info_type_list'),
    path('contact_info_type/new/', contact_info_type_views.contact_info_type_item, name='contact_info_type_new'),
    path('contact_info_type/<int:pk>/edit/', contact_info_type_views.contact_info_type_item, name='contact_info_type_edit'),
    path('contact_info_type/<int:pk>/delete/', contact_info_type_views.ContactInfoTypeDelete.as_view(), name='contact_info_type_delete'),

    path('employee/list/', employee_views.employee_list, name='employee_list'),
    path('employee/new/', employee_views.employee_item, name='employee_new'),
    path('employee/<int:pk>/edit/', employee_views.employee_item, name='employee_edit'),
    path('employee/<int:pk>/delete/', employee_views.EmployeeDelete.as_view(), name='employee_delete'),

    path('position/list/', position_views.position_list, name='position_list'),
    path('position/new/', position_views.position_item, name='position_new'),
    path('position/<int:pk>/edit/', position_views.position_item, name='position_edit'),
    path('position/<int:pk>/delete/', position_views.PositionDelete.as_view(), name='position_delete'),

    path('student/list/', student_views.student_list, name='student_list'),
    path('student/new/', student_views.student_item, name='student_new'),
    path('student/<int:pk>/edit/', student_views.student_item, name='student_edit'),
    path('student/<int:pk>/delete/', student_views.StudentDelete.as_view(), name='student_delete'),

    path('class_group/list/', class_group_views.class_group_list, name='class_group_list'),
    path('class_group/new/', class_group_views.class_group_item, name='class_group_new'),
    path('class_group/<int:pk>/edit/', class_group_views.class_group_item, name='class_group_edit'),
    path('class_group/<int:pk>/delete/', class_group_views.ClassGroupDelete.as_view(), name='class_group_delete'),

    path('class_group_enrollment/list/', class_group_enrollment_views.class_group_enrollment_list, name='class_group_enrollment_list'),
    path('class_group_enrollment/new/', class_group_enrollment_views.class_group_enrollment_item, name='class_group_enrollment_new'),
    path('class_group_enrollment/<int:pk>/edit/', class_group_enrollment_views.class_group_enrollment_item,
         name='class_group_enrollment_edit'),
    path('class_group_enrollment/<int:pk>/delete/', class_group_enrollment_views.ClassGroupEnrollmentDelete.as_view(),
         name='class_group_enrollment_delete'),

    path('pass_tag/list/', pass_tag_views.pass_tag_list, name='pass_tag_list'),
    path('pass_tag/new/', pass_tag_views.pass_tag_item, name='pass_tag_new'),
    path('pass_tag/<int:pk>/edit/', pass_tag_views.pass_tag_item, name='pass_tag_edit'),
    path('pass_tag/<int:pk>/delete/', pass_tag_views.PassTagDelete.as_view(), name='pass_tag_delete'),
    path('pass_tag/upload_csv/', pass_tag_views.pass_tag_upload_csv, name='pass_tag_upload_csv'),
    path('pass_tag/upload_csv_result/', TemplateView.as_view(template_name="entities/pass_tag/upload_csv_result.html"),
         name='pass_tag_upload_csv_result'),

    path('pass_tag_request/list/', pass_tag_request_views.pass_tag_request_list, name='pass_tag_request_list'),
    path('pass_tag_request/new/', pass_tag_request_views.pass_tag_request_item, name='pass_tag_request_new'),
    path('pass_tag_request/<int:pk>/edit/', pass_tag_request_views.pass_tag_request_item, name='pass_tag_request_edit'),
    path('pass_tag_request/<int:pk>/delete/', pass_tag_request_views.PassTagRequestDelete.as_view(), name='pass_tag_request_delete'),
    path('pass_tag_request/<int:pk>/export_csv/', pass_tag_request_views.pass_tag_request_export_csv, name='pass_tag_request_export_csv'),

]

