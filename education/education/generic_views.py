from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.forms import inlineformset_factory


def render_catalog_list(entity_model, columns, table_actions, row_actions, request):
    """Отображение веб-формы списка "справочника"."""
    template_name = 'catalog/list.html'
    context = {
        'username': request.user.username,
        'verbose_name_plural': entity_model._meta.verbose_name_plural,
        'columns': columns,
        'table_actions': table_actions,
        'row_actions': row_actions,
        'objects': entity_model.objects.all()
    }
    return render(request, template_name, context)


def render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=None, subtable_list=None, registry_list=None):
    """Отображение веб-формы элемента "справочника"/"документа"."""
    template_name = 'catalog/item.html'
    kwargs = {}
    subtable_factory_list = []
    if instance_pk is not None:
        instance = kwargs['instance'] = get_object_or_404(entity_model, pk=instance_pk)
        if subtable_list is not None:
            for subtable in subtable_list:
                subtable_factory_list.append(inlineformset_factory(
                    entity_model,
                    subtable['class'],
                    form=subtable['form_class'],
                    extra=subtable['extra_lines'],
                    can_delete=True
                ))
    formset_subtable_list = []
    if request.method == "POST":
        form = edit_form(request.POST, **kwargs)
        if instance_pk is not None and subtable_list is not None:
            for subtable_factory, subtable in zip(subtable_factory_list, subtable_list):
                formset = subtable_factory(request.POST, instance=instance)
                formset_subtable_list.append({'formset': formset, 'subtable': subtable})
        formset_list = []
        if instance_pk is not None and subtable_list is not None:
            for subtable_factory, subtable in zip(subtable_factory_list, subtable_list):
                formset = subtable_factory(request.POST, instance=instance)
                for formset_item in formset:
                    formset_item.fields[subtable['base_field']].required = False
                formset_list.append(formset)
        if form.is_valid() and ((instance_pk is None) or all(formset.is_valid() for formset in formset_list)):

            # Запись элемента "справочника"/"документа"
            instance = form.save(commit=False)
            instance.save()

            # Запись "табличных частей"
            for formset, subtable in zip(formset_list, subtable_list):
                for formset_item in formset:
                    if formset_item.instance.pk and formset_item.cleaned_data[subtable['base_field']] is None:
                        formset_item.instance.delete()
                items = formset.save()
                for item in items:
                    print(item)
                    print(getattr(item, subtable['base_field']))
                    if getattr(item, subtable['base_field']) is None:
                        item.delete()
                    else:
                        setattr(item, subtable['owner_field'], instance)
                        item.save()

            # Очистка "движений" по "регистрам"
            if registry_list is not None:
                for registry in registry_list:
                    registrar_filter = {registry['registrar_link_field']: instance}
                    registry['class'].objects.filter(**registrar_filter).delete()

            # Запись "движений" по "регистрам"
            if registry_list is not None:
                for registry in registry_list:
                    owner_filter = {registry['registrar_table_owner_link_field'] : instance}
                    subtable_items = registry['registrar_table_class'].objects.filter(**owner_filter)
                    for subtable_item in subtable_items:
                        registrar_filter = {registry['registrar_link_field']: instance}
                        for field_match in registry['field_matches']:
                            if field_match['from_table']:
                                registrar_filter[field_match['registrar_field']] = getattr(subtable_item, field_match['registry_field'])
                            else:
                                registrar_filter[field_match['registrar_field']] = getattr(instance, field_match['registry_field'])
                        registry['class'].objects.create(**registrar_filter)

            # Переход при окончании записи
            if request.POST.get('action') == 'save':
                return redirect(url_name + '_list')
            else:
                return redirect(url_name + '_edit', pk=instance.pk)
    else:
        form = edit_form(**kwargs)
        if instance_pk is not None and subtable_list is not None:
            for subtable_factory, subtable in zip(subtable_factory_list, subtable_list):
                formset = subtable_factory(instance=instance)
                formset_subtable_list.append({'formset': formset, 'subtable': subtable})

    # Создание контекста для веб-формы
    context = {
        'username': request.user.username,
        'verbose_name': entity_model._meta.verbose_name,
        'form': form,
        'fields': fields,
        'labels_width': labels_width,
        'back_url': reverse_lazy(url_name + '_list')
    }

    # Добавление контекста "табличных частей" к веб-форме
    if instance_pk is not None:
        context['formset_subtable_list'] = formset_subtable_list

    return render(request, template_name, context)
