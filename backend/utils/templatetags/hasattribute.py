from django import template

register = template.Library()


def hasattribute(value, arg):
    """Checks if an attribute of an object exists"""
    if hasattr(value, str(arg)):
        return True
    return False


register.filter('hasattribute', hasattribute)
