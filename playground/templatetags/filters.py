from django import template

register = template.Library()

@register.filter
def modulo(value, divisor):
    try:
        return value % divisor
    except (TypeError, ValueError):
        return 0