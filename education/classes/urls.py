from django.urls import path
from . import views

urlpatterns = [
    path('classes/student/list/', views.student_list, name='student_list'),
    path('classes/student/new/', views.student_new, name='student_new'),
    path('classes/student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('classes/student/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),

    path('classes/class_group/list/', views.class_group_list, name='class_group_list'),
    path('classes/class_group/new/', views.class_group_new, name='class_group_new'),
    path('classes/class_group/<int:pk>/edit/', views.class_group_edit, name='class_group_edit'),
    path('classes/class_group/<int:pk>/delete/', views.ClassGroupDelete.as_view(), name='class_group_delete'),

    path('classes/class_group_enrollment/list/', views.class_group_enrollment_list, name='class_group_enrollment_list'),
    path('classes/class_group_enrollment/new/', views.class_group_enrollment_new, name='class_group_enrollment_new'),
    path('classes/class_group_enrollment/<int:pk>/edit/', views.class_group_enrollment_edit, name='class_group_enrollment_edit'),
    path('classes/class_group_enrollment/<int:pk>/delete/', views.ClassGroupEnrollmentDelete.as_view(), name='class_group_enrollment_delete'),
]
