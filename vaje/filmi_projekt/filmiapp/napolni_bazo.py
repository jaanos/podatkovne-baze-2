import csv
from decimal import Decimal
from django.db import transaction
from filmiapp.models import Oseba, Film, Vloga, Zanr, Oznaka

def uvozi_osebe():
    """
    Skripta, ki uvozi osebe v podatkovno bazo.
    """

    print('Brisanje obstoječih oseb iz baze...')
    Oseba.objects.all().delete()

    # Pri programiranju imajo pogosto imena spremenljivk, ki so konstante velike črke 
    OSEBE_CSV = "podatki/oseba.csv"

    print(f'Uvažanje oseb iz {OSEBE_CSV} v bazo...')
    osebe = []
    with open(OSEBE_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) # preskočimo prvo vrstico (ime stolpcev)
        for row in reader:
            # Eksplicitno nastavimo id, da smo konzistentni s podatki
            id, ime = row
            osebe.append(
                Oseba(id=int(id), ime=ime)
            )
    """
    Zelo naiven način dodajanja v bazo:
    počasen, saj vsak klic .save() posebej commita v bazo!
    for oseba in osebe:
        oseba.save()
    """
    # Priročna funkcija, za hitro kreiranje in dodajanje v bazo
    Oseba.objects.bulk_create(osebe)

def uvozi_filme():
    """
    Skripta, ki uvozi filme v podatkovno bazo.
    """

    print('Brisanje obstoječih filmov iz baze...')
    Film.objects.all().delete()

    FILMI_CSV = "podatki/film.csv"

    print(f'Uvažanje filmov iz {FILMI_CSV} v bazo...')
    filmi = []
    # Filmi imajo tuj ključ na oznako - te bomo sproti po potrebi kreirali.
    # Oznak ni veliko in se večkrat ponavljajo. Da jih ne delamo na novo (pravzaprav ne bi bilo mogoče, saj je kratica primarni ključ),
    #  si jih shranimo v slovar:
    slovar_oznak = {} 
    with open(FILMI_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            # Ta način branja .csv-ja je nekoliko manj berljiv, ker imamo toliko stolpcev. 
            # Lepše bi bilo morda uporabiti csv.dictReader(f), ampak v to se ne bomo spuščali
            (id, naslov, dolzina, leto, ocena, 
             metascore, glasovi, zasluzek, 
             oznaka, opis) = row
            film = Film(
                id=int(id),
                naslov=naslov,
                dolzina=int(dolzina),
                leto=int(leto),
                ocena=Decimal(ocena)
            )
            # Preverimo še neobvezne stolpce
            if metascore:
                film.metascore = int(metascore)
            if glasovi:
                film.glasovi = int(glasovi)
            if zasluzek:
                film.zasluzek = int(zasluzek)
            if oznaka:
                if oznaka not in slovar_oznak:
                    slovar_oznak[oznaka] = Oznaka(kratica=oznaka)
                film.oznaka = slovar_oznak[oznaka]
            if opis:
                film.opis = opis
            filmi.append(film)
    # Prej je bilo zankanje in .save() zamudno, z transaction.atomic() pa je bolje
    with transaction.atomic():
        for oznaka in slovar_oznak.values(): # najprej shranimo oznake, saj jih imajo filmi kot tuj ključ.
            oznaka.save()
        for film in filmi:
            film.save() 

@transaction.atomic # transaction.atomic lahko uporabimo tudi kot decorator -> cela funkcija postane atomična operacija
def uvozi_zanre():
    """
    Skripta, ki uvozi žanre v podatkovno bazo.
    Treba je paziti, da so filmi že v bazi!
    Pozor: Ta funkcija vseeno ni zelo učinkovita, ker za vsako vrstico interagiramo z bazo.
    Bolje bi bilo, če bi filme pred zanko enkrat prebrali, za žanre pa morda spet imeli slovar.
    """

    print('Brisanje obstoječih žanrov iz baze...')
    Zanr.objects.all().delete()

    ZANRI_CSV = "podatki/zanr.csv"

    print(f'Uvažanje žanrov iz {ZANRI_CSV} v bazo...')
    with open(ZANRI_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id_filma, naziv = row
            film = Film.objects.get(id=int(id_filma))  # get enostavno vrne pripadajoč enoličen objekt, če je ta v bazi.
            zanr, _ = Zanr.objects.get_or_create(naziv=naziv)  # če Zanra z nazivom naziv ni v bazi, se bo objekt naredil in shranil v bazo.
            film.zanri.add(zanr)  # zanr dodamo v many-to-many relacijo z danim filmom. To se shrani tudi v bazo.

def uvozi_vloge():
    """
    Skripta, ki uvozi vloge v podatkovno bazo.
    """

    print('Brisanje obstoječih vlog iz baze...')
    Vloga.objects.all().delete()

    VLOGE_CSV = "podatki/vloga.csv"

    print(f'Uvažanje vlog iz {VLOGE_CSV} v bazo...')
    vloge = []

    filmi = Film.objects.in_bulk()
    osebe = Oseba.objects.in_bulk()
    # Zgornji dve metodi generirata priročna slovarja, ekvivalentno:
    # filmi = {film.id : film for film in Film.objects.all()}
    # osebe = {oseba.id : oseba for oseba in Oseba.objects.all()}
    with open(VLOGE_CSV, encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            id_filma, id_osebe, tip, mesto = row
            vloga = Vloga(
                film=filmi[int(id_filma)],
                oseba=osebe[int(id_osebe)],
                tip=tip,
                mesto=int(mesto)
            )
            vloge.append(vloga)
    Vloga.objects.bulk_create(vloge)
    
def main():
    uvozi_osebe()
    uvozi_filme()
    uvozi_zanre()
    uvozi_vloge()