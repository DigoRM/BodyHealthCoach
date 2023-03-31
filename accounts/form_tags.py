from django import template

register = template.Library()

@register.simple_tag
def render_field(form, field_name):
    field = form.fields.get(field_name)
    if field_name == 'peso' and form.instance.peso is not None:
        return ''
    return form[field_name]