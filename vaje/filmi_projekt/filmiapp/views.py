from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Film

"""
Testni pogled, ki smo ga naredili samo za prvo demonstracijo pogledov
def test(request):
    return HttpResponse("To je test.")
"""

def film_podrobnosti(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    polja = film._meta.get_fields()[2:] # Prvi dve polji sta vloga in id, ki nas ne zanimata
    podrobnosti = [(polje.verbose_name, getattr(film, polje.name)) for polje in polja]
    kontekst = {'film' : str(film), 'podrobnosti' : podrobnosti}
    return render(request, 'filmiapp/film_podrobnosti.html', kontekst)

def film_najboljsi(request, st_najboljsih):
    najboljsi = Film.objects.order_by('-ocena')[:st_najboljsih]
    info_najboljsi = [(f.id, f.naslov, f.ocena) for f in najboljsi]
    kontekst = {'info_najboljsi' : info_najboljsi, 'stevilo' : st_najboljsih}
    return render(request, 'filmiapp/film_najboljsi.html', kontekst)