from django import template
from ..models import Subscription
register = template.Library()

@register.filter(name='cansubscribe')
def cansubscribe(value, type, arg, search):

    return value