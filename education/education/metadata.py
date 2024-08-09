from django.apps import apps
from django.db.models import OneToOneField, PROTECT, RESTRICT

def has_dependencies(object):
    return check_dependencies(object, existence_only=True)

def get_dependencies(object):
    return check_dependencies(object, existence_only=False)

def check_dependencies(object, existence_only=False):
    """Получение описаний ссылок на объект по отношениям 1-1 и 1-N, препятствующих удалению объекта.
    Если значение параметра existence_only истинно, то возвращает булево значение, есть ли ссылки."""
    dependencies = {}
    for model in apps.get_models():
        for field in model._meta.get_fields():
            if field.is_relation and field.related_model == type(object):
                if (field.many_to_one or isinstance(field, OneToOneField)) and field.remote_field.on_delete in (PROTECT, RESTRICT):
                    related_objects = model.objects.filter(**{field.name: object})
                    if related_objects.exists():
                        if existence_only:
                            return True
                        dependencies[model._meta.verbose_name_plural] = [
                            {
                                'object': str(instance),
                                'fields': {field.verbose_name: getattr(instance, field.name, '')}
                            }
                            for instance in related_objects if not hasattr(instance, 'is_registry')
                        ]
    if existence_only:
        return False
    return dependencies
