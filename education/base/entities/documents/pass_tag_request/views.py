from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.http import HttpResponse

from ....generic_views import render_document_list, render_document_item

from ....entities.documents.pass_tag_request.models import PassTagRequest, PassTagRequestItem
from ....entities.documents.pass_tag_request.forms import PassTagRequestForm, PassTagRequestItemForm

import csv


class PassTagRequestDelete(DeleteView):
    model = PassTagRequest
    success_url = reverse_lazy('pass_tag_request_list')
    template_name = 'object_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_object()
        context['object_verbose_name'] = self.model._meta.verbose_name
        context['back_url'] = self.success_url
        return context


@login_required(login_url='/login/')
def pass_tag_request_list(request):
    entity_model = PassTagRequest
    url_name = 'pass_tag_request'
    columns = [
        {'name': 'presentation', 'title': 'Заявка', 'width': 15, 'type': 'text', 'sort': 'request_date', 'sort_type': 'date', 'link': url_name + '_edit'},
        {'name': 'comment', 'title': 'Комментарий', 'width': 28, 'type': 'text'},
        {'name': 'actions', 'title': 'Действия', 'width': 18, 'type': 'actions'}
    ]
    row_actions = [
        {'name': 'edit', 'title': 'Изменить', 'url': url_name + '_edit', 'button_class': 'btn-outline-primary'},
        {'name': 'to_csv', 'title': 'В CSV', 'url': url_name + '_export_csv', 'button_class': 'btn-outline-success'},
        {'name': 'delete', 'title': 'Удалить', 'url': url_name + '_delete', 'button_class': 'btn-outline-danger'}
    ]
    table_actions = [
        {'name': 'new', 'title': 'Добавить', 'url': url_name + '_new', 'button_class': 'btn-success'},
    ]
    return render_document_list(entity_model, columns, table_actions, row_actions, request)


@login_required(login_url='/login/')
def pass_tag_request_item(request, pk=None):
    entity_model = PassTagRequest
    edit_form = PassTagRequestForm
    url_name = 'pass_tag_request'
    fields = [
        {'name': 'number', 'title': 'Номер', 'width': 10},
        {'name': 'date', 'title': 'Дата', 'width': 10},
        {'name': 'requester', 'title': 'Заявитель', 'width': 28},
        {'name': 'executor', 'title': 'Исполнитель', 'width': 28},
        {'name': 'request_date', 'title': 'Дата заявки', 'width': 10},
        {'name': 'comment', 'title': 'Комментарий', 'width': 20},
    ]
    subtable_list = [
        {
            'title': 'Состав заявки',
            'class': PassTagRequestItem,
            'form_class': PassTagRequestItemForm,
            'extra_lines': 10,
            'base_field': 'holder',
            'owner_field': 'pass_tag_request',
            'fields': [
                {'name': 'holder', 'title': 'Держатель', 'width': 24},
                {'name': 'reason', 'title': 'Причина', 'width': 14},
                {'name': 'processing_date', 'title': 'Дата обработки', 'width': 10},
                {'name': 'pass_tag', 'title': 'Чип', 'width': 8},
                {'name': 'status', 'title': 'Статус', 'width': 12},
            ]
        }
    ]
    item_extra_actions = [
        {'name': 'to_csv', 'title': 'В CSV', 'url': url_name + '_export_csv', 'button_class': 'btn-outline-success'},
    ]
    labels_width = 12
    return render_document_item(
        entity_model,
        edit_form,
        url_name,
        fields,
        labels_width,
        request,
        instance_pk=pk,
        subtable_list=subtable_list,
        item_extra_actions=item_extra_actions
    )


@login_required(login_url='/login/')
def pass_tag_request_export_csv(request, pk=None):
    instance=PassTagRequest.objects.filter(pk=pk).first()
    file_name = f'{instance.pk}_{instance.date:%d.%m.%Y}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{file_name}"'
    writer = csv.writer(response)
    column_titles = [
        'ФИО', 'Табельный номер', 'Должность', 'Отдел', 'Номер пропуска', 'Примечание', 'Имя шаблона пропуска'
    ]
    writer.writerow(column_titles)
    request_items = PassTagRequestItem.objects.filter(pass_tag_request=instance)
    for request_item in request_items:
        holder = request_item.holder
        # Обучающиеся: класс, без отчества
        holder = f'{holder.last_name} {holder.first_name}'
        department = ''
        if hasattr(request_item.holder, 'rel_student'):
            class_group = request_item.holder.rel_student.class_group
            education_level = ''
            if 1 <= class_group.grade <= 4:
                education_level = 'Классы начальные'
            elif 5 <= class_group.grade <= 9:
                education_level = 'Классы средние'
            elif 10 <= class_group.grade <= 11:
                education_level = 'Классы старшие'
            else:
                education_level = 'Классы'
            department = f'Ученики,{education_level},{class_group}'
        # Сотрудники: основная должность
        main_position = ''
        if hasattr(request_item.holder, 'rel_employee'):
            main_position = request_item.holder.rel_employee.main_position
        if main_position != '' and department == '':
            department = 'Работники'
        row_data = [holder, '', '', department, request_item.pass_tag, '', '']
        writer.writerow(row_data)
    return response
