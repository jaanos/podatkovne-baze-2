from django import template

register = template.Library()

@register.filter
def je_glasoval(uporabnik, film):
    if not uporabnik.is_authenticated:
        return False
    return film.obstojeci_glasovi.filter(uporabnik=uporabnik).exists()