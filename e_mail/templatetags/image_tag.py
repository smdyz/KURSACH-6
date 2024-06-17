import datetime
from django import template

register = template.Library()


@register.simple_tag()
def image_tag(data):
    if data:
        return f'/media/{data}'
    return '#'


# @register.filter(needs_autoescape=True)
# def images_tag(data):
#     if data:
#         return f'media/{data}'
#     return '#'
