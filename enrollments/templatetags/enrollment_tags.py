from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Allow {{ dict|get_item:key }} in templates."""
    return dictionary.get(key)
