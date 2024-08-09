from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView

from ....metadata import get_dependencies
from ....generic_views import render_catalog_list, render_catalog_item

from ....objects.catalogs.student.models import Student
from ....objects.catalogs.student.forms import StudentForm


class StudentDelete(DeleteView):
    model = Student
    success_url = reverse_lazy('student_list')
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
def student_list(request):
    entity_model = Student
    url_name = 'student'
    columns = [
        {'name': 'title_without_status', 'title': 'Обучающийся', 'width': 36, 'type': 'number', 'link': url_name + '_edit'},
        {'name': 'class_group', 'title': 'Класс', 'width': 3, 'type': 'text'},
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
def student_item(request, pk=None):
    entity_model = Student
    edit_form = StudentForm
    url_name = 'student'
    fields = [
        {'name': 'individual', 'title': 'Физическое лицо', 'width': 36},
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, pk)
