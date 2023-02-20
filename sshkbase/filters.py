from django.template import Library

register = Library()


# This function is a template filter : it can be used inside templates like this : "value|get_item:key"
# It returns the element in list 'value' at index 'key'
@register.filter
def get_item(value, key):
    return value[key]
