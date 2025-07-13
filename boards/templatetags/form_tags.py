from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Añade la clase CSS `css_class` al widget HTML del campo `field`.
    Uso en plantilla: {{ form.field|add_class:"form-control" }}
    """
    return field.as_widget(attrs={"class": css_class})