from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from ....views import render_page as render
from ....metadata import get_dependencies
from ....generic_views import render_catalog_list, render_catalog_item

from ....entities.catalogs.contact_info_type.models import ContactInfoType
from ....entities.catalogs.contact_info_type.forms import ContactInfoTypeForm


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
    entity_model = ContactInfoType
    url_name = 'contact_info_type'
    columns = [
        {'name': 'title', 'title': 'Наименование', 'width': 16, 'type': 'text', 'link': url_name + '_edit'},
        {'name': 'actions', 'title': 'Действия', 'width': 20, 'type': 'actions'}
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
def contact_info_type_item(request, pk=None):
    entity_model = ContactInfoType
    edit_form = ContactInfoTypeForm
    url_name = 'contact_info_type'
    fields = [
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'title', 'title': 'Наименование', 'width': 12},
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk)
