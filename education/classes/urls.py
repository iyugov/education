from django.urls import path
from . import views

urlpatterns = [
    path('student/list/', views.student_list, name='student_list'),
    path('student/new/', views.student_new, name='student_new'),
    path('student/<int:pk>/edit/', views.student_edit, name='student_edit'),
    path('student/<int:pk>/delete/', views.StudentDelete.as_view(), name='student_delete'),

    path('class_group/list/', views.class_group_list, name='class_group_list'),
    path('class_group/new/', views.class_group_new, name='class_group_new'),
    path('class_group/<int:pk>/edit/', views.class_group_edit, name='class_group_edit'),
    path('class_group/<int:pk>/delete/', views.ClassGroupDelete.as_view(), name='class_group_delete'),

    path('class_group_enrollment/list/', views.class_group_enrollment_list, name='class_group_enrollment_list'),
    path('class_group_enrollment/new/', views.class_group_enrollment_new, name='class_group_enrollment_new'),
    path('class_group_enrollment/<int:pk>/edit/', views.class_group_enrollment_edit, name='class_group_enrollment_edit'),
    path('class_group_enrollment/<int:pk>/delete/', views.ClassGroupEnrollmentDelete.as_view(), name='class_group_enrollment_delete'),
]
