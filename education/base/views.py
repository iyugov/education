from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, views as auth_views
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory
from django.db.models import Q

# Create your views here.

import csv
import io

from textwrap import shorten
from datetime import datetime

from .models import social_insurance_number_validator, Individual, ContactInfoType, ContactInfoItem, Gender
from .forms import IndividualForm, ContactInfoTypeForm, ContactInfoItemForm, CustomAuthForm, IndividualCSVUploadForm
from education.metadata import get_dependencies

class CSVImportException(Exception):
    def __init__(self, message):
        self.message = message

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

def individual_upload_csv(request):
    back_link = 'individual_list'
    back_url = reverse_lazy(back_link)
    error_message = ''
    if request.method == 'POST':
        form = IndividualCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            success_flag = True
            upload_report = []
            valid_individual_data = []
            print()
            try:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                file_line_count = 1
                raw_data_keys = ['last_name', 'first_name', 'patronymic', 'gender', 'birth_date', 'social_insurance_number', 'comment']
                for line in csv.reader(io_string, delimiter=',', quotechar='"'):
                    file_line_count += 1
                    error_prefix = f'Строка {file_line_count}: '
                    if len(line) != len(raw_data_keys):
                        raise CSVImportException
                    raw_data = {key : value.strip() for key, value in zip(raw_data_keys, line)}
                    try:
                        if raw_data['last_name'] == '':
                            raise CSVImportException(f'{error_prefix}пустая фамилия.')
                        print(len(raw_data['last_name']))
                        if len(raw_data['last_name']) > Individual._meta.get_field('last_name').max_length:
                            raise CSVImportException(f'{error_prefix}слишком длинная фамилия: {shorten(raw_data_keys['last_name'])}.')
                        if raw_data['first_name'] == '':
                            raise CSVImportException(f'{error_prefix}пустое имя.')
                        if len(raw_data['first_name']) > Individual._meta.get_field('first_name').max_length:
                            raise CSVImportException(f'{error_prefix}слишком длинное имя: {shorten(raw_data_keys['first_name'])}.')
                        if len(raw_data['patronymic']) > Individual._meta.get_field('patronymic').max_length:
                            raise CSVImportException(f'{error_prefix}слишком длинное отчество: {shorten(raw_data_keys['patronymic'])}.')
                        gender = raw_data['gender'].upper()
                        if gender in ('', '-', 'НЕ УКАЗАН'):
                            raw_data['gender'] = Gender.objects.get(title='Не указан')
                        elif gender in ('ЖЕНСКИЙ', 'ЖЕН', 'Ж'):
                            raw_data['gender'] = Gender.objects.get(title='Женский')
                        elif gender in ('МУЖСКОЙ', 'МУЖ', 'М'):
                            raw_data['gender'] = Gender.objects.get(title='Мужской')
                        else:
                            raise CSVImportException(f'{error_prefix}неверный пол: {shorten(raw_data_keys['gender'])}.')
                        if raw_data['birth_date'] != '':
                            try:
                                raw_data['birth_date'] = datetime.strptime(raw_data['birth_date'], '%d.%m.%Y')
                            except ValueError:
                                raise CSVImportException(f'{error_prefix}неверная дата рождения для формата "ДД.ММ.ГГГГ": {shorten(raw_data_keys['birth_date'])}.')
                        if raw_data['social_insurance_number'] != '':
                            try:
                                social_insurance_number_validator(raw_data['social_insurance_number'])
                            except ValueError:
                                raise CSVImportException(f'{error_prefix}неверное значение СНИЛС: {shorten(raw_data_keys['social_insurance_number'])}.')
                        if len(raw_data['comment']) > Individual._meta.get_field('comment').max_length:
                            raise CSVImportException(
                                f'{error_prefix}слишком длинный комментарий: {shorten(raw_data_keys['comment'])}.')
                    except CSVImportException as e:
                        success_flag = False
                        error_message = e.message
                        break
                    else:
                        valid_individual_data.append(raw_data)
            except Exception:
                success_flag = False
                error_message = 'Файл имеет неверный формат.'
            if success_flag and not valid_individual_data:
                success_flag = False
                error_message = 'Файл не содержит данных для физических лиц.'
            if success_flag:
                unique_pks = set()
                unique_social_insurance_numbers = set()
                for valid_individual in valid_individual_data:
                    social_insurance_number = valid_individual['social_insurance_number']
                    if social_insurance_number:
                        instance = Individual.objects.filter(social_insurance_number=social_insurance_number)
                        if social_insurance_number in unique_social_insurance_numbers:
                            individual = instance.first()
                            individual_data = {
                                'name': str(individual),
                                'birth_date': individual.birth_date,
                                'social_insurance_number': individual.social_insurance_number
                            }
                            upload_report.append(
                                {'individual': individual_data, 'result': 'Повторяется в файле; пропущено.', 'class': 'table-warning'})
                        else:
                            if instance.exists():
                                individual = instance.first()
                                individual_data = {
                                    'name': str(individual),
                                    'birth_date': individual.birth_date,
                                    'social_insurance_number': ''
                                }
                                upload_report.append(
                                    {'individual': individual_data, 'result': 'Физическое лицо уже существует; пропущено.', 'class': 'table-info'})
                                unique_pks.add(individual.pk)
                                unique_social_insurance_numbers.add(individual.social_insurance_number)
                            else:
                                individual = Individual.objects.create(
                                    last_name=valid_individual['last_name'],
                                    first_name=valid_individual['first_name'],
                                    patronymic=valid_individual['patronymic'],
                                    gender=valid_individual['gender'],
                                    social_insurance_number=valid_individual['social_insurance_number'],
                                    comment=valid_individual['comment'],
                                )
                                if valid_individual['birth_date']:
                                     individual.birth_date = valid_individual['birth_date']
                                individual_data = {
                                    'name': str(individual),
                                    'birth_date': individual.birth_date,
                                    'social_insurance_number': individual.social_insurance_number
                                }
                                upload_report.append({'individual': individual_data, 'result': 'Физическое лицо создано.', 'class': 'table-success'})
                                unique_pks.add(individual.pk)
                                unique_social_insurance_numbers.add(individual.social_insurance_number)
                    else:
                        if valid_individual['birth_date']:
                            individuals = Individual.objects.filter(
                                Q(last_name=valid_individual['last_name']) &
                                Q(first_name=valid_individual['first_name']) &
                                Q(patronymic=valid_individual['patronymic']) &
                                Q(birth_date=valid_individual['birth_date'])
                            )
                        else:
                            individuals = Individual.objects.filter(
                                Q(last_name=valid_individual['last_name']) &
                                Q(first_name=valid_individual['first_name']) &
                                Q(patronymic=valid_individual['patronymic'])
                            )
                        if len(individuals) == 0:
                            if valid_individual['birth_date']:
                                individual = Individual.objects.create(
                                    last_name=valid_individual['last_name'],
                                    first_name=valid_individual['first_name'],
                                    patronymic=valid_individual['patronymic'],
                                    gender=valid_individual['gender'],
                                    birth_date=valid_individual['birth_date'],
                                    comment=valid_individual['comment'],
                                )
                            else:
                                individual = Individual.objects.create(
                                    last_name=valid_individual['last_name'],
                                    first_name=valid_individual['first_name'],
                                    patronymic=valid_individual['patronymic'],
                                    gender=valid_individual['gender'],
                                    comment=valid_individual['comment'],
                                )
                            individual_data = {
                                'name': str(individual),
                                'birth_date': individual.birth_date,
                                'social_insurance_number': individual.social_insurance_number
                            }
                            upload_report.append({'individual': individual_data, 'result': 'Физическое лицо создано.',
                                                  'class': 'table-success'})
                            unique_pks.add(individual.pk)
                            unique_social_insurance_numbers.add(individual.social_insurance_number)
                        elif len(individuals) == 1:
                            individual = individuals.first()
                            individual_data = {
                                'name': str(individual),
                                'birth_date': individual.birth_date,
                                'social_insurance_number': individual.social_insurance_number
                            }
                            if individual.pk in unique_pks:
                                upload_report.append(
                                    {'individual': individual_data, 'result': 'Повторяется в файле; пропущено.',
                                     'class': 'table-warning'})
                            else:
                                upload_report.append(
                                    {'individual': individual_data, 'result': 'Физическое лицо уже существует; пропущено.',
                                     'class': 'table-info'})
                            unique_pks.add(individual.pk)
                            unique_social_insurance_numbers.add(individual.social_insurance_number)
                        else:
                            individual = individuals.first()
                            individual_data = {
                                'name': str(individual),
                                'birth_date': individual.birth_date,
                                'social_insurance_number': individual.social_insurance_number
                            }
                            upload_report.append(
                                {'individual': individual_data, 'result': 'Физические лица уже существуют; пропущено.',
                                 'class': 'table-warning'})
                            unique_pks.add(individual.pk)
                            unique_social_insurance_numbers.add(individual.social_insurance_number)
            context = {
                'username': request.user.username,
                'form': form,
                'back_url': back_url,
                'success': success_flag,
                'report': upload_report,
                'error_message': error_message}
            return render(request, 'entities/individual/upload_csv_result.html', context)
    else:
        form = IndividualCSVUploadForm()
    return render(request, 'entities/individual/upload_csv.html', {'username': request.user.username, 'form': form, 'back_url': back_url})



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

