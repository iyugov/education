from django.urls import path
from . import views

urlpatterns = [

    path('pass_cards/pass_card_action/list/', views.pass_card_action_list, name='pass_card_action_list'),
    path('pass_cards/pass_card_action/new/', views.pass_card_action_new, name='pass_card_action_new'),
    path('pass_cards/pass_card_action/<int:pk>/edit/', views.pass_card_action_edit, name='pass_card_action_edit'),
    path('pass_cards/pass_card_action/<int:pk>/delete/', views.PassCardActionDelete.as_view(), name='pass_card_action_delete'),
    
    path('pass_cards/pass_card_type/list/', views.pass_card_type_list, name='pass_card_type_list'),
    path('pass_cards/pass_card_type/new/', views.pass_card_type_new, name='pass_card_type_new'),
    path('pass_cards/pass_card_type/<int:pk>/edit/', views.pass_card_type_edit, name='pass_card_type_edit'),
    path('pass_cards/pass_card_type/<int:pk>/delete/', views.PassCardTypeDelete.as_view(), name='pass_card_type_delete'),
    
    path('pass_cards/pass_card/list/', views.pass_card_list, name='pass_card_list'),
    path('pass_cards/pass_card/new/', views.pass_card_new, name='pass_card_new'),
    path('pass_cards/pass_card/<int:pk>/edit/', views.pass_card_edit, name='pass_card_edit'),
    path('pass_cards/pass_card/<int:pk>/delete/', views.PassCardDelete.as_view(), name='pass_card_delete'),
    
    path('pass_cards/pass_card_issue/list/', views.pass_card_issue_list, name='pass_card_issue_list'),
    path('pass_cards/pass_card_issue/new/', views.pass_card_issue_new, name='pass_card_issue_new'),
    path('pass_cards/pass_card_issue/<int:pk>/edit/', views.pass_card_issue_edit, name='pass_card_issue_edit'),
    path('pass_cards/pass_card_issue/<int:pk>/delete/', views.PassCardIssueDelete.as_view(), name='pass_card_issue_delete'),
]
