from django import template

register = template.Library()


@register.filter
def get_item(mapping, key):
    """
    Template filter to get a value from a mapping by variable key.
    Usage: {{ mydict|get_item:var }}
    """
    try:
        return mapping.get(key)
    except Exception:
        try:
            return mapping[key]
        except Exception:
            return None
