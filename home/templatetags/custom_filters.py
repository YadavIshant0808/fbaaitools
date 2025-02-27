from django import template

register = template.Library()

@register.filter(name='contains_table')
def contains_table(value):
    """Returns True if '<table' is found in the value."""
    if not isinstance(value, str):
        return False
    return '<table' in value.lower()
