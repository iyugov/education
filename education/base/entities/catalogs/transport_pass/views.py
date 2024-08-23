from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ....generic_views import render_catalog_list, render_catalog_item, EntityDeleteView

from ....entities.catalogs.transport_pass.models import TransportPass
from ....entities.catalogs.transport_pass.forms import TransportPassForm


class TransportPassDelete(EntityDeleteView):
    model = TransportPass
    success_url = reverse_lazy('transport_pass_list')


@login_required(login_url='/login/')
def transport_pass_list(request):
    entity_model = TransportPass
    url_name = 'transport_pass'
    columns = [
        {'name': 'pass_id', 'title': 'Номер', 'width': 20, 'type': 'text', 'link': url_name + '_edit'},
        {'name': 'actions', 'title': 'Действия', 'width': 24, 'type': 'actions'}
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
def transport_pass_item(request, pk=None):
    entity_model = TransportPass
    edit_form = TransportPassForm
    url_name = 'transport_pass'
    fields = [
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'pass_id', 'title': 'Номер', 'width': 13},
    ]
    labels_width = 6
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk)
