from django import template

register = template.Library()


@register.filter
def with_data_original(field):
    """Render form field with data-original set to its value, preserving all existing attrs."""
    widget = field.field.widget
    attrs = widget.attrs.copy()  # Keep all existing attributes
    print(attrs,"attrs")
    value = field.value()

    # Add data-original
    attrs["data-original"] = value if value is not None else ""

    return field.as_widget(attrs=attrs)