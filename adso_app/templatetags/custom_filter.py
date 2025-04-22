from django import template
import os

register = template.Library()

@register.filter
def file_type_icon(file_url):
    _, ext = os.path.splitext(file_url.lower())

    if ext in ['.jpg', '.jpeg', '.png']:
        return 'imagen'
    elif ext == '.pdf':
        return 'pdf'
    elif ext in ['.doc', '.docx']:
        return 'word'
    else:
        return 'otro'