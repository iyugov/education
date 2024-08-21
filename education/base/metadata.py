from django.apps import apps
from django.db.models import OneToOneField, PROTECT, RESTRICT
import inspect
import base.entities.catalogs as catalogs
import base.entities.documents as documents
import base.entities.enumerations as enumerations

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


def get_entities_data():
    entity_packages = (catalogs, documents, enumerations)
    entities_data = []
    for entity_package in entity_packages:
        for package_name, package in inspect.getmembers(entity_package, predicate=inspect.ismodule):
            modules = dict(inspect.getmembers(package, predicate=inspect.ismodule))
            if 'views' in modules:
                views_module = modules['views']
            else:
                views_module = None
            if 'models' in modules:
                models_module = modules['models']
                for model_class_name, model_class in inspect.getmembers(models_module, predicate=inspect.isclass):
                    if hasattr(model_class, 'entity_name'):
                        entity_data = {'class': model_class, 'entity_name': model_class.entity_name}
                        if views_module is not None:
                            entity_data['views_module'] = views_module
                        entities_data.append(entity_data)
    return entities_data
