from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ....generic_views import render_catalog_list, render_catalog_item, EntityDeleteView

from ....entities.catalogs.student.models import Student
from ....entities.catalogs.student.forms import StudentForm


class StudentDelete(EntityDeleteView):
    model = Student
    success_url = reverse_lazy('student_list')


@login_required(login_url='/login/')
def student_list(request):
    entity_model = Student
    url_name = 'student'
    columns = [
        {'name': 'title_without_status', 'title': 'Обучающийся', 'width': 36, 'type': 'text', 'link': url_name + '_edit'},
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
        {'name': 'code', 'title': 'Код', 'width': 6},
        {'name': 'individual', 'title': 'Физическое лицо', 'width': 36},
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, pk)
