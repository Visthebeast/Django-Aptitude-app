from django import template
import math

register = template.Library()

@register.filter
def modulo(value, divisor):
    try:
        return value % divisor
    except (TypeError, ValueError):
        return 0

@register.filter
def div(value,divisor):
    try:
        return math.floor(value/divisor)
    except (TypeError, ValueError):
        return 0

@register.filter(name='zero_pad')
def zero_pad(value):
    try:
        return str(value).zfill(2)
    except ValueError:
        return value