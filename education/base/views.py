from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views as auth_views
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory

# Create your views here.

from .models import Individual, ContactInfoType, ContactInfoItem
from .forms import IndividualForm, ContactInfoTypeForm, ContactInfoItemForm, CustomAuthForm
from education.metadata import get_dependencies


class IndividualDelete(DeleteView):
    model = Individual
    success_url = reverse_lazy('individual_list')
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['object_verbose_name'] = self.model._meta.verbose_name
        context['back_url'] = self.success_url
        return context

    def get(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        dependencies = get_dependencies(object_to_delete)
        context = {
            'username': request.user.username,
            'object': object_to_delete,
            'object_verbose_name': self.model._meta.verbose_name,
            'dependencies': dependencies,
            'back_url': self.success_url
        }
        if dependencies != {}:
            return render(request, 'object_cannot_delete.html', context)
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def individual_list(request):
    individuals = Individual.objects.all()
    return render(request, 'entities/individual/list.html', {'username': request.user.username, 'individual_list': individuals})


@login_required(login_url='/login/')
def individual_new(request):
    back_link = 'individual_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = IndividualForm(request.POST)
        if form.is_valid():
            individual = form.save(commit=False)
            individual.save()
            return redirect(back_link)
    else:
        form = IndividualForm()
    return render(request, 'entities/individual/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def individual_edit(request, pk):
    back_link = 'individual_list'
    back_url = reverse_lazy(back_link)
    individual = get_object_or_404(Individual, pk=pk)
    ContactInfoItemFormSet = inlineformset_factory(
        Individual, ContactInfoItem, form=ContactInfoItemForm, extra=1, can_delete=True
    )
    if request.method == 'POST':
        form = IndividualForm(request.POST, instance=individual)
        formset = ContactInfoItemFormSet(request.POST, instance=individual)
        for formset_item in formset:
            formset_item.fields['contact_info_type'].required = False
        print(formset.errors)
        if form.is_valid() and formset.is_valid():

            individual = form.save(commit=False)
            individual.save()
            for formset_item in formset:
                if formset_item.instance.pk and formset_item.cleaned_data['contact_info_type'] is None:
                    formset_item.instance.delete()
            items = formset.save()
            for item in items:
                if item.contact_info_type is None:
                    item.delete()
                else:
                    item.individual = individual
                    item.save()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('individual_edit', pk=pk)
    else:
        form = IndividualForm(instance=individual)
        formset = ContactInfoItemFormSet(instance=individual)
    return render(request, 'entities/individual/edit.html', {'username': request.user.username, 'form': form, 'formset': formset, 'back_url': back_url})


class ContactInfoTypeDelete(DeleteView):
    model = ContactInfoType
    success_url = reverse_lazy('contact_info_type_list')
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['object_verbose_name'] = self.model._meta.verbose_name
        context['back_url'] = self.success_url
        return context

    def get(self, request, *args, **kwargs):
        object_to_delete = self.get_object()
        dependencies = get_dependencies(object_to_delete)
        context = {
            'username': request.user.username,
            'object': object_to_delete,
            'object_verbose_name': self.model._meta.verbose_name,
            'dependencies': dependencies,
            'back_url': self.success_url
        }
        if dependencies != {}:
            return render(request, 'object_cannot_delete.html', context)
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def contact_info_type_list(request):
    contact_info_types = ContactInfoType.objects.all()
    return render(request, 'entities/contact_info_type/list.html', {'username': request.user.username, 'contact_info_type_list': contact_info_types})


@login_required(login_url='/login/')
def contact_info_type_new(request):
    back_link = 'contact_info_type_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = ContactInfoTypeForm(request.POST)
        if form.is_valid():
            contact_info_type = form.save(commit=False)
            contact_info_type.save()
            return redirect(back_link)
    else:
        form = ContactInfoTypeForm()
    return render(request, 'entities/contact_info_type/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def contact_info_type_edit(request, pk):
    back_link = 'contact_info_type_list'
    back_url = reverse_lazy(back_link)
    contact_info_type = get_object_or_404(ContactInfoType, pk=pk)
    if request.method == 'POST':
        form = ContactInfoTypeForm(request.POST, instance=contact_info_type)
        if form.is_valid():
            contact_info_type = form.save(commit=False)
            contact_info_type.save()
            return redirect(back_link)
    else:
        form = ContactInfoTypeForm(instance=contact_info_type)
    return render(request, 'entities/contact_info_type/edit.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


class CustomLoginView(auth_views.LoginView):
    authentication_form = CustomAuthForm


def user_logout(request):
    logout(request)
    return redirect('login')


def home(request):
    return render(request, 'base.html', {'username': request.user.username})

