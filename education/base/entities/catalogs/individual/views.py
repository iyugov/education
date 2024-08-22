from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.db.models import Q

from datetime import datetime

from ....views import render_page as render
from ....metadata import get_dependencies
from ....generic_views import render_catalog_list, render_catalog_item

from ....entities.enumerations.gender.models import Gender
from ....entities.catalogs.individual.models import Individual, ContactInfoItem, social_insurance_number_validator
from ....entities.catalogs.student.models import Student
from ....entities.catalogs.individual.forms import IndividualForm, ContactInfoItemForm, IndividualCSVUploadForm

import csv
import io
from textwrap import shorten


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
    entity_model = Individual
    url_name = 'individual'
    columns = [
        {'name': 'last_name', 'title': 'Фамилия', 'width': 12, 'type': 'text', 'link': url_name + '_edit'},
        {'name': 'first_name', 'title': 'Имя', 'width': 12, 'type': 'text'},
        {'name': 'patronymic', 'title': 'Отчество', 'width': 12, 'type': 'text'},
        {'name': 'gender', 'title': 'Пол', 'width': 6, 'type': 'text'},
        {'name': 'birth_date', 'title': 'Дата рождения', 'width': 6, 'type': 'date', 'sort': 'birth_date', 'sort_type': 'date'},
        {'name': 'comment', 'title': 'Комментарий', 'width': 16, 'type': 'text'},
        {'name': 'actions', 'title': 'Действия', 'width': 12, 'type': 'actions'}
    ]
    row_actions = [
        {'name': 'edit', 'title': 'Изменить', 'url': url_name + '_edit', 'button_class': 'btn-outline-primary'},
        {'name': 'delete', 'title': 'Удалить', 'url': url_name + '_delete', 'button_class': 'btn-outline-danger'}
    ]
    table_actions = [
        {'name': 'new', 'title': 'Добавить', 'url': url_name + '_new', 'button_class': 'btn-success'},
        {'name': 'upload_csv', 'title': 'Из CSV', 'url': url_name + '_upload_csv', 'button_class': 'btn-outline-success'}
    ]
    return render_catalog_list(entity_model, columns, table_actions, row_actions, request)


@login_required(login_url='/login/')
def individual_item(request, pk=None):
    entity_model = Individual
    edit_form = IndividualForm
    url_name = 'individual'
    fields = [
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'last_name', 'title': 'Фамилия', 'width': 14},
        {'name': 'first_name', 'title': 'Имя', 'width': 14},
        {'name': 'patronymic', 'title': 'Отчество', 'width': 14},
        {'name': 'birth_date', 'title': 'Дата рождения', 'width': 10},
        {'name': 'gender', 'title': 'Пол', 'width': 8},
        {'name': 'social_insurance_number', 'title': 'СНИЛС', 'width': 11},
        {'name': 'comment', 'title': 'Комментарий', 'width': 20},
    ]
    subtable_list = [
        {
            'title': 'Контактная информация',
            'class': ContactInfoItem,
            'form_class': ContactInfoItemForm,
            'extra_lines': 3,
            'base_field': 'contact_info_type',
            'owner_field': 'individual',
            'fields': [
                {'name': 'contact_info_type', 'title': 'Тип', 'width': 12},
                {'name': 'value', 'title': 'Значение', 'width': 14},
                {'name': 'comment', 'title': 'Комментарий', 'width': 20},
            ]
        }
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk, subtable_list=subtable_list)

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
                set_students = form.cleaned_data.get('set_students')
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
                                if set_students and not hasattr(individual, 'student'):
                                    Student.objects.create(individual=individual)
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
                            if set_students and not hasattr(individual, 'student'):
                                Student.objects.create(individual=individual)
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
