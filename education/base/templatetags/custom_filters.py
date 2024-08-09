from django import template

register = template.Library()


@register.filter
def get_attribute(value, arg):
    return getattr(value, arg)


@register.filter
def get_form_field(form, field_name):
    return form[field_name]


@register.filter
def total_width(columns):
    return sum(column['width'] for column in columns)
