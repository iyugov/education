from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView


from ....generic_views import render_catalog_list, render_catalog_item

from ....objects.documents.pass_tag_request.models import PassTagRequest, PassTagRequestItem
from ....objects.documents.pass_tag_request.forms import PassTagRequestForm, PassTagRequestItemForm


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
        {'name': 'actions', 'title': 'Действия', 'width': 12, 'type': 'actions'}
    ]
    row_actions = [
        {'name': 'edit', 'title': 'Изменить', 'url': url_name + '_edit', 'button_class': 'btn-outline-primary'},
        {'name': 'delete', 'title': 'Удалить', 'url': url_name + '_delete', 'button_class': 'btn-outline-danger'}
    ]
    table_actions = [
        {'name': 'new', 'title': 'Добавить', 'url': url_name + '_new', 'button_class': 'btn-success'}
    ]
    return render_catalog_list(entity_model, columns, table_actions, row_actions, request)


@login_required(login_url='/login/')
def pass_tag_request_item(request, pk=None):
    entity_model = PassTagRequest
    edit_form = PassTagRequestForm
    url_name = 'pass_tag_request'
    fields = [
        {'name': 'requester', 'title': 'Заявитель', 'width': 24},
        {'name': 'executor', 'title': 'Исполнитель', 'width': 24},
        {'name': 'request_date', 'title': 'Дата заявки', 'width': 10},
        {'name': 'comment', 'title': 'Комментарий', 'width': 20},
    ]
    subtable_list = [
        {
            'title': 'Контактная информация',
            'class': PassTagRequestItem,
            'form_class': PassTagRequestItemForm,
            'extra_lines': 3,
            'base_field': 'holder',
            'owner_field': 'pass_tag_request',
            'fields': [
                {'name': 'holder', 'title': 'Тип', 'width': 24},
                {'name': 'reason', 'title': 'Причина', 'width': 14},
                {'name': 'processing_date', 'title': 'Дата обработки', 'width': 10},
                {'name': 'pass_tag', 'title': 'Чип', 'width': 8},
                {'name': 'status', 'title': 'Статус', 'width': 12},
            ]
        }
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk, subtable_list=subtable_list)
