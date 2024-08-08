from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory

# Create your views here.

from .models import Student, ClassGroup, ClassGroupEnrollment, ClassGroupEnrollmentItem, ClassGroupEnrollmentRegistryItem
from .forms import StudentForm, ClassGroupForm, ClassGroupEnrollmentForm, ClassGroupEnrollmentItemForm

from education.metadata import get_dependencies
from education.generic_views import render_catalog_list, render_catalog_item


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


class ClassGroupDelete(DeleteView):
    model = ClassGroup
    success_url = reverse_lazy('class_group_list')
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
def class_group_list(request):
    entity_model = ClassGroup
    url_name = 'class_group'
    columns = [
        {'name': 'presentation', 'title': 'Класс', 'width': 6, 'type': 'number', 'link': url_name + '_edit'},
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
        {'name': 'grade', 'title': 'Параллель', 'width': 8},
        {'name': 'label', 'title': 'Литера', 'width': 10},
    ]
    labels_width = 10
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk)


class ClassGroupEnrollmentDelete(DeleteView):
    model = ClassGroupEnrollment
    success_url = reverse_lazy('class_group_enrollment_list')
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
        ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=object_to_delete).delete()
        return super().get(request, *args, **kwargs)


@login_required(login_url='/login/')
def class_group_enrollment_list(request):
    entity_model = ClassGroupEnrollment
    url_name = 'class_group_enrollment'
    columns = [
        {'name': 'presentation', 'title': 'Зачисление', 'width': 15, 'type': 'text', 'sort': 'enrollment_date', 'sort_type': 'date', 'link': url_name + '_edit'},
        {'name': 'actions', 'title': 'Действия', 'width': 30, 'type': 'actions'}
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
def class_group_enrollment_new(request):
    back_link = 'class_group_enrollment_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = ClassGroupEnrollmentForm(request.POST)
        if form.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=class_group_enrollment).delete()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('class_group_enrollment_edit', pk=class_group_enrollment.pk)
    else:
        form = ClassGroupEnrollmentForm()
    return render(request, 'entities/class_group_enrollment/item.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def class_group_enrollment_edit(request, pk):
    back_link = 'class_group_enrollment_list'
    back_url = reverse_lazy(back_link)
    class_group_enrollment = get_object_or_404(ClassGroupEnrollment, pk=pk)
    PassTagRequestItemFormSet = inlineformset_factory(
        ClassGroupEnrollment, ClassGroupEnrollmentItem, form=ClassGroupEnrollmentItemForm, extra=40, can_delete=True
    )
    if request.method == 'POST':
        form = ClassGroupEnrollmentForm(request.POST, instance=class_group_enrollment)
        formset = PassTagRequestItemFormSet(request.POST, instance=class_group_enrollment)
        for formset_item in formset:
            formset_item.fields['student'].required = False
        if form.is_valid() and formset.is_valid():
            class_group_enrollment = form.save(commit=False)
            class_group_enrollment.save()
            ClassGroupEnrollmentRegistryItem.objects.filter(class_group_enrollment=class_group_enrollment).delete()
            for formset_item in formset:
                if formset_item.instance.pk and formset_item.cleaned_data['student'] is None:
                    formset_item.instance.delete()
            items = formset.save()
            print(items)
            for item in items:
                if item.student is None:
                    item.delete()
                else:
                    item.class_group_enrollment = class_group_enrollment
                    item.save()
            class_group_enrollment_items = ClassGroupEnrollmentItem.objects.filter(class_group_enrollment=class_group_enrollment)
            for class_group_enrollment_item in class_group_enrollment_items:
                    ClassGroupEnrollmentRegistryItem.objects.create(
                        class_group_enrollment=class_group_enrollment,
                        enrollment_date=class_group_enrollment.enrollment_date,
                        student=class_group_enrollment_item.student,
                        class_group=class_group_enrollment_item.class_group
                    )
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('class_group_enrollment_edit', pk=pk)
    else:
        form = ClassGroupEnrollmentForm(instance=class_group_enrollment)
        formset = PassTagRequestItemFormSet(instance=class_group_enrollment)
    return render(request, 'entities/class_group_enrollment/item.html', {'username': request.user.username, 'form': form, 'formset': formset, 'back_url': back_url})
