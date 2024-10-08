from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy

from ....generic_views import render_document_list, render_document_item, EntityDeleteView

from ....entities.documents.class_group_enrollment.models import ClassGroupEnrollment, ClassGroupEnrollmentItem
from ....entities.registries.class_group_enrollment_registry.models import ClassGroupEnrollmentRegistryItem
from ....entities.documents.class_group_enrollment.forms import ClassGroupEnrollmentForm, ClassGroupEnrollmentItemForm


class ClassGroupEnrollmentDelete(EntityDeleteView):
    model = ClassGroupEnrollment
    success_url = reverse_lazy('class_group_enrollment_list')
    registry_list = [
        {
            'class': ClassGroupEnrollmentRegistryItem,
            'registrar_link_field': 'class_group_enrollment',
        }
    ]


@login_required(login_url='/login/')
def class_group_enrollment_list(request):
    entity_model = ClassGroupEnrollment
    url_name = 'class_group_enrollment'
    columns = [
        {'name': 'presentation', 'title': 'Зачисление', 'width': 15, 'type': 'text', 'sort': 'enrollment_date', 'sort_type': 'date', 'link': url_name + '_edit'},
        {'name': 'comment', 'title': 'Комментарий', 'width': 20, 'type': 'text'},
        {'name': 'actions', 'title': 'Действия', 'width': 12, 'type': 'actions'}
    ]
    row_actions = [
        {'name': 'edit', 'title': 'Изменить', 'url': url_name + '_edit', 'button_class': 'btn-outline-primary'},
        {'name': 'delete', 'title': 'Удалить', 'url': url_name + '_delete', 'button_class': 'btn-outline-danger'}
    ]
    table_actions = [
        {'name': 'new', 'title': 'Добавить', 'url': url_name + '_new', 'button_class': 'btn-success'}
    ]
    return render_document_list(entity_model, columns, table_actions, row_actions, request)


@login_required(login_url='/login/')
def class_group_enrollment_item(request, pk=None):
    entity_model = ClassGroupEnrollment
    edit_form = ClassGroupEnrollmentForm
    url_name = 'class_group_enrollment'
    fields = [
        {'name': 'number', 'title': 'Номер', 'width': 10},
        {'name': 'date', 'title': 'Дата', 'width': 10},
        {'name': 'enrollment_date', 'title': 'Дата зачисления', 'width': 10},
        {'name': 'comment', 'title': 'Комментарий', 'width': 20},
    ]
    registry_list = [
        {
            'class': ClassGroupEnrollmentRegistryItem,
            'registrar_table_class': ClassGroupEnrollmentItem,
            'registrar_link_field': 'class_group_enrollment',
            'registrar_table_owner_link_field': 'class_group_enrollment',
            'field_matches': [
                {'registry_field': 'enrollment_date', 'registrar_field': 'enrollment_date', 'from_table': False},
                {'registry_field': 'student', 'registrar_field': 'student', 'from_table': True},
                {'registry_field': 'class_group', 'registrar_field': 'class_group', 'from_table': True},
            ]
        },
    ]
    subtable_list = [
        {
            'title': 'Зачисления',
            'class': ClassGroupEnrollmentItem,
            'form_class': ClassGroupEnrollmentItemForm,
            'extra_lines': 50,
            'base_field': 'student',
            'owner_field': 'class_group_enrollment',
            'fields': [
                {'name': 'student', 'title': 'Обучающийся', 'width': 30},
                {'name': 'class_group', 'title': 'Класс', 'width': 6},
            ]
        }
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
        registry_list=registry_list,
    )
