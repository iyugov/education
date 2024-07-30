from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views as auth_views
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory


# Create your views here.

from .models import Individual, ContactInfoType, ContactInfoItem
from .forms import IndividualForm, ContactInfoTypeForm, ContactInfoItemForm, CustomAuthForm

from pass_cards.models import PassCardIssue
from classes.models import Student


class IndividualDelete(DeleteView):
    model = Individual
    success_url = reverse_lazy('individual_list')
    template_name = 'entities/individual/confirm_delete.html'
    
    def get(self, request, *args, **kwargs):
        individual = self.get_object()
        pass_card_issues = []
        dependencies = PassCardIssue.objects.filter(individual=individual)
        if dependencies.exists():
            pass_card_issues = [str(dependency) for dependency in dependencies]
        students = []
        dependencies = Student.objects.filter(individual=individual)
        if dependencies.exists():
            students = [str(dependency) for dependency in dependencies]
        if pass_card_issues or students:
            return render(request, 'entities/individual/cannot_delete.html', {'username': request.user.username, 'individual': individual, 'pass_card_issue_list': pass_card_issues, 'student_list': students})
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def individual_list(request):
    individuals = Individual.objects.all()
    return render(request, 'entities/individual/list.html', {'username': request.user.username, 'individual_list': individuals})


@login_required(login_url='/login/')
def individual_new(request):
    if request.method == "POST":
        form = IndividualForm(request.POST)
        if form.is_valid():
            individual = form.save(commit=False)
            individual.save()
            return redirect('individual_list')
    else:
        form = IndividualForm()
    return render(request, 'entities/individual/edit.html', {'username': request.user.username, 'form': form})


@login_required(login_url='/login/')
def individual_edit(request, pk):
    individual = get_object_or_404(Individual, pk=pk)
    ContactInfoItemFormSet = inlineformset_factory(
        Individual, ContactInfoItem, form=ContactInfoItemForm, extra=3, can_delete=True
    )
    if request.method == 'POST':
        form = IndividualForm(request.POST, instance=individual)
        formset = ContactInfoItemFormSet(request.POST, instance=individual)
        if form.is_valid() and formset.is_valid():
            individual = form.save(commit=False)
            individual.save()
            formset.save()
            return redirect('individual_list')
    else:
        form = IndividualForm(instance=individual)
        formset = ContactInfoItemFormSet(instance=individual)
    return render(request, 'entities/individual/edit.html', {'username': request.user.username, 'form': form, 'formset': formset})


class ContactInfoTypeDelete(DeleteView):
    model = ContactInfoType
    success_url = reverse_lazy('contact_info_type_list')
    template_name = 'entities/contact_info_type/confirm_delete.html'

    def get(self, request, *args, **kwargs):
        contact_info_type = self.get_object()
        contact_info_items = []
        dependencies = ContactInfoItem.objects.filter(contact_info_type=contact_info_type)
        if dependencies.exists():
            contact_info_items = [str(dependency) for dependency in dependencies]
        if contact_info_items:
            return render(request, 'entities/contact_info_type/cannot_delete.html', {'username': request.user.username, 'contact_info_type': contact_info_type, 'contact_info_item_list': contact_info_items})
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def contact_info_type_list(request):
    contact_info_types = ContactInfoType.objects.all()
    return render(request, 'entities/contact_info_type/list.html', {'username': request.user.username, 'contact_info_type_list': contact_info_types})


@login_required(login_url='/login/')
def contact_info_type_new(request):
    if request.method == "POST":
        form = ContactInfoTypeForm(request.POST)
        if form.is_valid():
            contact_info_type = form.save(commit=False)
            contact_info_type.save()
            return redirect('contact_info_type_list')
    else:
        form = ContactInfoTypeForm()
    return render(request, 'entities/contact_info_type/edit.html', {'username': request.user.username, 'form': form})


@login_required(login_url='/login/')
def contact_info_type_edit(request, pk):
    contact_info_type = get_object_or_404(ContactInfoType, pk=pk)
    if request.method == 'POST':
        form = ContactInfoTypeForm(request.POST, instance=contact_info_type)
        if form.is_valid():
            contact_info_type = form.save(commit=False)
            contact_info_type.save()
            return redirect('contact_info_type_list')
    else:
        form = ContactInfoTypeForm(instance=contact_info_type)
    return render(request, 'entities/contact_info_type/edit.html', {'username': request.user.username, 'form': form})


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'base.html', {'username': request.user.username})

