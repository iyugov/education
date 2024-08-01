from django.apps import apps

def get_dependencies(object):
    """Получение описаний ссылок на объект по отношениям 1-1 и 1-N."""
    dependencies = {}
    # Проходимся по всем моделям в проекте
    for model in apps.get_models():
        # Проходимся по всем полям модели
        for field in model._meta.get_fields():
            # Ищем внешние ключи
            if field.is_relation and field.many_to_one and field.related_model == type(object):
                related_objects = model.objects.filter(**{field.name: object})
                if related_objects.exists():
                    dependencies[model._meta.verbose_name_plural] = [
                        {
                            'object': str(instance),
                            'fields': {field.verbose_name: getattr(instance, field.name, '')}
                        }
                        for instance in related_objects
                    ]
    return dependencies
