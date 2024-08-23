from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ....generic_views import render_catalog_list, render_catalog_item, EntityDeleteView

from ....entities.catalogs.position.models import Position
from ....entities.catalogs.position.forms import PositionForm


class PositionDelete(EntityDeleteView):
    model = Position
    success_url = reverse_lazy('position_list')


@login_required(login_url='/login/')
def position_list(request):
    entity_model = Position
    url_name = 'position'
    columns = [
        {'name': 'title', 'title': 'Наименование', 'width': 20, 'type': 'text', 'link': url_name + '_edit'},
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
def position_item(request, pk=None):
    entity_model = Position
    edit_form = PositionForm
    url_name = 'position'
    fields = [
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'title', 'title': 'Наименование', 'width': 36},
    ]
    subtable_list = []
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk, subtable_list=subtable_list)
