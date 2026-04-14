from django import template
from ..models import DaniGlasovi

register = template.Library()

@register.filter
def je_glasoval(uporabnik, film):
    if not uporabnik.is_authenticated:
        return False
    return DaniGlasovi.objects.filter(uporabnik=uporabnik, film=film).exists()