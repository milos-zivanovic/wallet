from django import template

register = template.Library()


@register.filter
def trim_email(value):
    return value.split('@')[0] if '@' in value else value
