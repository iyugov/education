from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy


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


def render_catalog_item(entity_model, edit_form, url_name, fields, labels_width, request, instance_pk=None):
    """Отображение веб-формы элемента "справочника"."""
    template_name = 'catalog/item.html'
    kwargs = {}
    if instance_pk is not None:
        kwargs['instance'] = get_object_or_404(entity_model, pk=instance_pk)
    if request.method == "POST":
        form = edit_form(request.POST, **kwargs)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            return redirect(url_name + '_list')
    else:
        form = edit_form(**kwargs)
    context = {
        'username': request.user.username,
        'verbose_name': entity_model._meta.verbose_name,
        'form': form,
        'fields': fields,
        'labels_width': labels_width,
        'back_url': reverse_lazy(url_name + '_list')
    }
    print(dir(form))
    return render(request, template_name, context)
