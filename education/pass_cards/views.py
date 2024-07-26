from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import JsonResponse


# Create your views here.

from .models import PassCardAction, PassCardType, PassCard, PassCardIssue
from .forms import PassCardActionForm, PassCardTypeForm, PassCardForm, PassCardIssueForm

# Действие с пропускными картами

class PassCardActionDelete(DeleteView):
    model = PassCardAction
    success_url = reverse_lazy('pass_card_actions')
    template_name = 'pass_card_action_confirm_delete.html'
    
    def get(self, request, *args, **kwargs):
        pass_card_action = self.get_object()
        pass_card_issues = []
        dependences = PassCardIssue.objects.filter(action=pass_card_action)
        if dependences.exists():
            pass_card_issues = [str(dependency) for dependency in dependences]
        if pass_card_issues:
            return render(request, 'pass_card_action_cannot_delete.html', {'pass_card_action': pass_card_action, 'pass_card_issues': pass_card_issues})
        return super().get(request, *args, **kwargs)

@login_required(login_url='/login/')
def pass_card_actions_list(request):
    pass_card_actions = PassCardAction.objects.all()
    return render(request, 'pass_card_actions_list.html', {'pass_card_actions': pass_card_actions})

@login_required(login_url='/login/')
def pass_card_action_new(request):
    if request.method == "POST":
        form = PassCardActionForm(request.POST)
        if form.is_valid():
            pass_card_action = form.save(commit=False)
            pass_card_action.save()
            return redirect('pass_card_actions')
    else:
        form = PassCardActionForm()
    return render(request, 'pass_card_action_edit.html', {'form': form})

@login_required(login_url='/login/')
def pass_card_action_edit(request, pk):
    pass_card_action = get_object_or_404(PassCardAction, pk=pk)
    if request.method == 'POST':
        form = PassCardActionForm(request.POST, instance=pass_card_action)
        if form.is_valid():
            pass_card_action = form.save(commit=False)
            pass_card_action.save()
            return redirect('pass_card_actions')
    else:
        form = PassCardActionForm(instance=pass_card_action)
    return render(request, 'pass_card_action_edit.html', {'form': form})

# Тип пропускной карты

class PassCardTypeDelete(DeleteView):
    model = PassCardType
    success_url = reverse_lazy('pass_card_types')
    template_name = 'pass_card_type_confirm_delete.html'
    
    def get(self, request, *args, **kwargs):
        pass_card_type = self.get_object()
        pass_cards = []
        dependences = PassCard.objects.filter(pass_type=pass_card_type)
        if dependences.exists():
            pass_cards = [str(dependency) for dependency in dependences]
        if pass_cards:
            return render(request, 'pass_card_type_cannot_delete.html', {'pass_card_type': pass_card_type, 'pass_cards': pass_cards})
        return super().get(request, *args, **kwargs)

@login_required(login_url='/login/')
def pass_card_types_list(request):
    pass_card_types = PassCardType.objects.all()
    return render(request, 'pass_card_types_list.html', {'pass_card_types': pass_card_types})

@login_required(login_url='/login/')
def pass_card_type_new(request):
    if request.method == "POST":
        form = PassCardTypeForm(request.POST)
        if form.is_valid():
            pass_card_type = form.save(commit=False)
            pass_card_type.save()
            return redirect('pass_card_types')
    else:
        form = PassCardTypeForm()
    return render(request, 'pass_card_type_edit.html', {'form': form})

@login_required(login_url='/login/')
def pass_card_type_edit(request, pk):
    pass_card_type = get_object_or_404(PassCardType, pk=pk)
    if request.method == 'POST':
        form = PassCardTypeForm(request.POST, instance=pass_card_type)
        if form.is_valid():
            pass_card_type = form.save(commit=False)
            pass_card_type.save()
            return redirect('pass_card_types')
    else:
        form = PassCardTypeForm(instance=pass_card_type)
    return render(request, 'pass_card_type_edit.html', {'form': form})

# Пропускная карта

class PassCardDelete(DeleteView):
    model = PassCard
    success_url = reverse_lazy('pass_cards')
    template_name = 'pass_card_confirm_delete.html'
    
    def get(self, request, *args, **kwargs):
        pass_card = self.get_object()
        pass_card_issues = []
        dependences = PassCardIssue.objects.filter(card=pass_card)
        if dependences.exists():
            pass_card_issues = [str(dependency) for dependency in dependences]
        if pass_card_issues:
            return render(request, 'pass_card_cannot_delete.html', {'pass_card': pass_card, 'pass_card_issues': pass_card_issues})
        return super().get(request, *args, **kwargs)

@login_required(login_url='/login/')
def pass_cards_list(request):
    pass_cards = PassCard.objects.all()
    return render(request, 'pass_cards_list.html', {'pass_cards': pass_cards})

@login_required(login_url='/login/')
def pass_card_new(request):
    if request.method == "POST":
        form = PassCardForm(request.POST)
        if form.is_valid():
            pass_card = form.save(commit=False)
            pass_card.save()
            return redirect('pass_cards')
    else:
        form = PassCardForm()
    return render(request, 'pass_card_edit.html', {'form': form})

@login_required(login_url='/login/')
def pass_card_edit(request, pk):
    pass_card = get_object_or_404(PassCard, pk=pk)
    if request.method == 'POST':
        form = PassCardForm(request.POST, instance=pass_card)
        if form.is_valid():
            pass_card = form.save(commit=False)
            pass_card.save()
            return redirect('pass_cards')
    else:
        form = PassCardForm(instance=pass_card)
    return render(request, 'pass_card_edit.html', {'form': form})

# Оформление пропускной карты

class PassCardIssueDelete(DeleteView):
    model = PassCardIssue
    success_url = reverse_lazy('pass_card_issues')
    template_name = 'pass_card_issue_confirm_delete.html'

@login_required(login_url='/login/')
def pass_card_issues_list(request):
    pass_card_issues = PassCardIssue.objects.all()
    return render(request, 'pass_card_issues_list.html', {'pass_card_issues': pass_card_issues})

@login_required(login_url='/login/')
def pass_card_issue_new(request):
    if request.method == "POST":
        form = PassCardIssueForm(request.POST)
        if form.is_valid():
            pass_card_issue = form.save(commit=False)
            pass_card_issue.save()
            return redirect('pass_card_issues')
    else:
        form = PassCardIssueForm()
    return render(request, 'pass_card_issue_edit.html', {'form': form})

@login_required(login_url='/login/')
def pass_card_issue_edit(request, pk):
    pass_card_issue = get_object_or_404(PassCardIssue, pk=pk)
    if request.method == 'POST':
        form = PassCardIssueForm(request.POST, instance=pass_card_issue)
        if form.is_valid():
            pass_card_issue = form.save(commit=False)
            pass_card_issue.save()
            return redirect('pass_card_issues')
    else:
        form = PassCardIssueForm(instance=pass_card_issue)
    return render(request, 'pass_card_issue_edit.html', {'form': form})
