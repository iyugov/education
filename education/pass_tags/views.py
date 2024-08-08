from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView
from django.forms import inlineformset_factory

import csv
import io
from textwrap import shorten

# Create your views here.

from .models import PassTag, PassTagRequest, PassTagRequestItem, tag_id_validator
from .forms import PassTagForm, PassTagRequestForm, PassTagRequestItemForm, PassTagCSVUploadForm

from education.metadata import get_dependencies
from education.generic_views import render_catalog_list, render_catalog_item

class PassTagDelete(DeleteView):
    model = PassTag
    success_url = reverse_lazy('pass_tag_list')
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
def pass_tag_list(request):
    entity_model = PassTag
    url_name = 'pass_tag'
    columns = [
        {'name': 'tag_id', 'title': 'Идентификатор', 'width': 16, 'type': 'text', 'link': url_name + '_edit'},
        {'name': 'actions', 'title': 'Действия', 'width': 20, 'type': 'actions'}
    ]
    row_actions = [
        {'name': 'edit', 'title': 'Изменить', 'url': url_name + '_edit', 'button_class': 'btn-outline-primary'},
        {'name': 'delete', 'title': 'Удалить', 'url': url_name + '_delete', 'button_class': 'btn-outline-danger'}
    ]
    table_actions = [
        {'name': 'new', 'title': 'Добавить', 'url': url_name + '_new', 'button_class': 'btn-success'},
        {'name': 'upload_csv', 'title': 'Из CSV', 'url': url_name + '_upload_csv', 'button_class': 'btn-outline-success'}
    ]
    return render_catalog_list(entity_model, columns, table_actions, row_actions, request)


@login_required(login_url='/login/')
def pass_tag_item(request, pk=None):
    entity_model = PassTag
    edit_form = PassTagForm
    url_name = 'pass_tag'
    fields = [
        {'name': 'tag_id', 'title': 'Идентификатор', 'width': 8},
    ]
    labels_width = 12
    return render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=pk)


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
def pass_tag_request_new(request):
    back_link = 'pass_tag_request_list'
    back_url = reverse_lazy(back_link)
    if request.method == "POST":
        form = PassTagRequestForm(request.POST)
        if form.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('pass_tag_request_edit', pk=pass_tag_request.pk)
    else:
        form = PassTagRequestForm()
    return render(request, 'entities/pass_tag_request/item.html', {'username': request.user.username, 'form': form, 'back_url': back_url})


@login_required(login_url='/login/')
def pass_tag_request_edit(request, pk):
    back_link = 'pass_tag_request_list'
    back_url = reverse_lazy(back_link)
    pass_tag_request = get_object_or_404(PassTagRequest, pk=pk)
    PassTagRequestItemFormSet = inlineformset_factory(
        PassTagRequest, PassTagRequestItem, form=PassTagRequestItemForm, extra=1, can_delete=True
    )

    if request.method == 'POST':
        form = PassTagRequestForm(request.POST, instance=pass_tag_request)
        formset = PassTagRequestItemFormSet(request.POST, instance=pass_tag_request)
        for formset_item in formset:
            formset_item.fields['holder'].required = False
        if form.is_valid() and formset.is_valid():
            pass_tag_request = form.save(commit=False)
            pass_tag_request.save()
            for formset_item in formset:
                if formset_item.instance.pk and formset_item.cleaned_data['holder'] is None:
                    formset_item.instance.delete()
            items = formset.save()
            for item in items:
                if item.holder is None:
                    item.delete()
                else:
                    item.pass_tag_request = pass_tag_request
                    item.save()
            if request.POST.get('action') == 'save':
                return redirect(back_link)
            else:
                return redirect('pass_tag_request_edit', pk=pk)
    else:
        form = PassTagRequestForm(instance=pass_tag_request)
        formset = PassTagRequestItemFormSet(instance=pass_tag_request)
    return render(request, 'entities/pass_tag_request/item.html', {'username': request.user.username, 'form': form, 'formset': formset, 'back_url': back_url})


def pass_tag_upload_csv(request):
    back_link = 'pass_tag_list'
    back_url = reverse_lazy(back_link)
    error_message = ''
    if request.method == 'POST':
        form = PassTagCSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            success_flag = True
            upload_report = []
            valid_tag_ids = []
            try:
                data_set = csv_file.read().decode('UTF-8')
                io_string = io.StringIO(data_set)
                next(io_string)
                for line in csv.reader(io_string, delimiter=',', quotechar='"'):
                    tag_id = line[0].strip()
                    try:
                        tag_id_validator(tag_id)
                    except:
                        success_flag = False
                        error_message = f'Неверный идентификатор: {shorten(tag_id, width=9, placeholder='...')}'
                        break
                    else:
                        valid_tag_ids.append(tag_id)
            except Exception:
                success_flag = False
                error_message = 'Файл имеет неверный формат.'
            if success_flag and not valid_tag_ids:
                success_flag = False
                error_message = 'Файл не содержит данных для идентификаторов.'
            if success_flag:
                unique_ids = set()
                for tag_id in valid_tag_ids:
                    if tag_id in unique_ids:
                        upload_report.append({'tag_id': tag_id, 'result': 'Повторяется в файле; пропущен.', 'class': 'table-warning'})
                    else:
                        if PassTag.objects.filter(tag_id=tag_id).exists():
                            upload_report.append(
                                {'tag_id': tag_id, 'result': 'Чип уже существует; пропущен.', 'class': 'table-info'})
                        else:
                            PassTag.objects.create(tag_id=tag_id)
                            upload_report.append({'tag_id': tag_id, 'result': 'Чип создан.', 'class': 'table-success'})
                            unique_ids.add(tag_id)
            context = {
                'username': request.user.username,
                'form': form,
                'back_url': back_url,
                'success': success_flag,
                'report': upload_report,
                'error_message': error_message}
            return render(request, 'entities/pass_tag/upload_csv_result.html', context)
    else:
        form = PassTagCSVUploadForm()
    return render(request, 'entities/pass_tag/upload_csv.html', {'username': request.user.username, 'form': form, 'back_url': back_url})
