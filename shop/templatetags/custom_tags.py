from django import template
from .. models import ProductAttribute
register = template.Library()

@register.simple_tag
def get_obj(pk,attr):
    obj = getattr(ProductAttribute.objects.get(pk=int(pk)), attr)
    return obj
