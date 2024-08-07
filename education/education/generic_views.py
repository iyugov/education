from django.shortcuts import render


def render_catalog_list(entity_model, columns, table_actions, row_actions, request):
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
