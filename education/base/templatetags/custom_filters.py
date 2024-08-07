from django import template

register = template.Library()


@register.filter
def getattribute(value, arg):
    return getattr(value, arg)


@register.filter
def total_width(columns):
    return sum(column['width'] for column in columns)
