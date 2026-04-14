from django.shortcuts import redirect, render, get_object_or_404
from django.db import transaction
from django.http import HttpResponseNotAllowed
from django.db.models import F
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from .models import Film, Oseba, DaniGlasovi
from .forms import FilmForm, OsebaForm

"""
Testni pogled, ki smo ga naredili samo za prvo demonstracijo pogledov
def test(request):
    return HttpResponse("To je test.")
"""

def index(request):
    return render(request, 'filmiapp/index.html', {})


def film_podrobnosti(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    kontekst = {'film' : film}
    return render(request, 'filmiapp/film_podrobnosti.html', kontekst)


def film_najboljsi(request, st_najboljsih):
    najboljsi = Film.objects.order_by('-ocena')[:st_najboljsih]
    info_najboljsi = [(f.id, f.naslov, f.ocena) for f in najboljsi]
    kontekst = {'info_najboljsi' : info_najboljsi, 'stevilo' : st_najboljsih}
    return render(request, 'filmiapp/film_najboljsi.html', kontekst)

def film_poisci(request):
    poizvedba = request.GET.get('zacetek', '')
    zeleni_filmi = []
    if poizvedba:
        zeleni_filmi = Film.objects.filter(naslov__istartswith=poizvedba)[:100]
    return render(request, 'filmiapp/film_poisci.html', {'poizvedba' : poizvedba, 'rezultat' : zeleni_filmi})

@login_required
@transaction.atomic
def film_glasuj(request):
    if request.method == 'POST':
        film_id = request.POST.get('film_id', -1)
        film = get_object_or_404(Film, id=film_id)
        user = request.user
        glas, ustvarjen = DaniGlasovi.objects.get_or_create(uporabnik=user, film=film)
        ze_glasoval = not ustvarjen
        if ze_glasoval:
            messages.success(request, "Odstranili ste svoj glas.")
            glas.delete()
            film.glasovi = F('glasovi') - 1
        else:
            film.glasovi = F('glasovi') + 1
            messages.success(request, "Vaš glas je bil zabeležen!")
        
        film.save()
        return redirect('filmiapp:film_podrobnosti', film_id)
    return HttpResponseNotAllowed(['POST'])

@permission_required('filmiapp.add_film')
@transaction.atomic
def film_dodaj(request):
    if request.method == "POST":
        form = FilmForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('filmiapp:film_podrobnosti', film_id=form.instance.pk)
    else:
        form = FilmForm()
    kontekst = {'form': form}
    return render(request, 'filmiapp/film_dodaj.html', kontekst)

@permission_required('filmiapp.change_film')
@transaction.atomic
def film_uredi(request, film_id):
    film = get_object_or_404(Film, id=film_id)
    if request.method == "POST":
        form = FilmForm(request.POST, instance=film)
        if form.is_valid():
            form.save()
            return redirect('filmiapp:film_podrobnosti', film_id=form.instance.pk)
    else:
        form = FilmForm(instance=film)
    kontekst = {'form': form}
    return render(request, 'filmiapp/film_uredi.html', kontekst)

def oseba_poisci(request):
    poizvedba = request.GET.get('zacetek', '')
    zelene_osebe = []
    if poizvedba:
        zelene_osebe = Oseba.objects.filter(ime__istartswith=poizvedba)[:100]
    return render(request, 'filmiapp/oseba_poisci.html', {'poizvedba' : poizvedba, 'rezultat' : zelene_osebe})

def oseba_podrobnosti(request, oseba_id):
    oseba = get_object_or_404(Oseba, id=oseba_id)
    kontekst = {'oseba' : oseba}
    return render(request, 'filmiapp/oseba_podrobnosti.html', kontekst)

@permission_required('filmiapp.change_oseba')
@transaction.atomic
def oseba_uredi(request, oseba_id):
    oseba = get_object_or_404(Oseba, id=oseba_id)
    if request.method == "POST":
        form = OsebaForm(request.POST, instance=oseba)
        if form.is_valid():
            form.save()
            return redirect('filmiapp:oseba_podrobnosti', oseba_id=form.instance.pk)
    else:
        form = OsebaForm(instance=oseba)
    kontekst = {'form': form}
    return render(request, 'filmiapp/oseba_uredi.html', kontekst)

@permission_required('filmiapp.add_oseba')
@transaction.atomic
def oseba_dodaj(request):
    if request.method == "POST":
        form = OsebaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('filmiapp:oseba_podrobnosti', oseba_id=form.instance.pk)
    else:
        form = OsebaForm()
    kontekst = {'form': form}
    return render(request, 'filmiapp/oseba_dodaj.html', kontekst)

@transaction.atomic
def registracija(request):
    if request.user.is_authenticated:
        return redirect('filmiapp:index')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request, form.instance)
            messages.success(request, f"Uporabnik {form.instance.username} uspešno registriran!")
            return redirect('filmiapp:index')
    else:
        form = UserCreationForm()
    kontekst = {'form': form}
    return render(request, 'registration/registration.html', kontekst)
