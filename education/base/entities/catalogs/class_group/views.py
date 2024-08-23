from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ....generic_views import render_catalog_list, render_catalog_item, EntityDeleteView

from ....entities.catalogs.class_group.models import ClassGroup
from ....entities.catalogs.class_group.forms import ClassGroupForm


class ClassGroupDelete(EntityDeleteView):
    model = ClassGroup
    success_url = reverse_lazy('class_group_list')


@login_required(login_url='/login/')
def class_group_list(request):
    entity_model = ClassGroup
    url_name = 'class_group'
    columns = [
        {'name': 'presentation', 'title': 'Класс', 'width': 6, 'type': 'number', 'sort': 'grade',
         'sort_type': 'number', 'link': url_name + '_edit'},
        {'name': 'actions', 'title': 'Действия', 'width': 42, 'type': 'actions'}
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
def class_group_item(request, pk=None):
    entity_model = ClassGroup
    edit_form = ClassGroupForm
    url_name = 'class_group'
    fields = [
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'grade', 'title': 'Параллель', 'width': 8},
        {'name': 'label', 'title': 'Литера', 'width': 10},
    ]
    labels_width = 10
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk)
