from django.urls import path
from . import views

urlpatterns = [

    path('pass_cards/pass_card_actions/', views.pass_card_actions_list, name='pass_card_actions'),
    path('pass_cards/pass_card_actions/new/', views.pass_card_action_new, name='pass_card_action_new'),
    path('pass_cards/pass_card_actions/<int:pk>/edit/', views.pass_card_action_edit, name='pass_card_action_edit'),
    path('pass_cards/pass_card_actions/<int:pk>/delete/', views.PassCardActionDelete.as_view(), name='pass_card_action_delete'),
    
    path('pass_cards/pass_card_types/', views.pass_card_types_list, name='pass_card_types'),
    path('pass_cards/pass_card_types/new/', views.pass_card_type_new, name='pass_card_type_new'),
    path('pass_cards/pass_card_types/<int:pk>/edit/', views.pass_card_type_edit, name='pass_card_type_edit'),
    path('pass_cards/pass_card_types/<int:pk>/delete/', views.PassCardTypeDelete.as_view(), name='pass_card_type_delete'),
    
    path('pass_cards/pass_cards/', views.pass_cards_list, name='pass_cards'),
    path('pass_cards/pass_cards/new/', views.pass_card_new, name='pass_card_new'),
    path('pass_cards/pass_cards/<int:pk>/edit/', views.pass_card_edit, name='pass_card_edit'),
    path('pass_cards/pass_cards/<int:pk>/delete/', views.PassCardDelete.as_view(), name='pass_card_delete'),
    
    path('pass_cards/pass_card_issues/', views.pass_card_issues_list, name='pass_card_issues'),
    path('pass_cards/pass_card_issues/new/', views.pass_card_issue_new, name='pass_card_issue_new'),
    path('pass_cards/pass_card_issues/<int:pk>/edit/', views.pass_card_issue_edit, name='pass_card_issue_edit'),
    path('pass_cards/pass_card_issues/<int:pk>/delete/', views.PassCardIssueDelete.as_view(), name='pass_card_issue_delete'),
]
