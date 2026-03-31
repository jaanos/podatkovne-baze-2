---
marp: true
style: "@import url('style.css')"
---

<span class="hidden">{% raw %}</span>

# Django

* [Django](https://www.djangoproject.com/) je ogrodje za razvoj spletnih aplikacij, ki vključuje:
  * preslikavo med objekti in relacijskimi podatkovnimi bazami (ORM),
  * vgrajen skrbniški vmesnik,
  * sistem za predloge, in
  * podporo za internacionalizacijo.

---

# Projekti in aplikacije

* Posamezen projekt v Djangu sestoji iz ene ali več aplikacij.
* Projekt ustvarimo z ukazom
  ```bash
  django-admin startproject IME_PROJEKTA IME_MAPE
  ```
* Ustvari se mapa s podanim imenom in znotraj nje:
  - `manage.py`: glavni program za delo s projektom
  - `IME_PROJEKTA/`: mapa z glavnim modulom projekta
    + `__init__.py`: prazna datoteka, ki določa modul
    + `settings.py`: datoteka z nastavitvami
    + `urls.py`: specifikacije poti
    + `asgi.py`, `wsgi.py`: vstopni točki za različne spletne strežnike

---

# Program `manage.py`

* Program `manage.py` lahko kličemo kot
  ```bash
  python manage.py UKAZ ...
  ```
* Nekaj pogosto uporabljenih ukazov:
  * `runserver`: požene razvojni spletni strežnik
  * `makemigrations`: ustvari migracije glede na spremembe modela
  * `migrate`: požene migracije, da spravi bazo v stanje, konsistentno z modelom
  * `createsuperuser`: ustvari račun za skrbnika
  * `shell`: požene ukazno vrstico z naloženim projektom

---

# Aplikacije

* Aplikacijo ustvarimo z ukazom
  ```bash
  python manage.py startapp APLIKACIJA
  ```
* Ustvari se mapa `APLIKACIJA` z vsebino:
  - `__init__.py`: prazna datoteka, ki določa modul
  - `admin.py`: skrbniški vmesnik
  - `models.py`: podatkovni model
  - `tests.py`: testi
  - `views.py`: pogledi (logika aplikacije)
  - `migrations/`: mapa z migracijami
    + `__init__.py`

---

# Nastavitve - `settings.py`

* Nastavitve projekta se nahajajo v programu `settings.py`.
  * To je privzeti program, ki se vključi v `manage.py`/`asgi.py`/`wsgi.py`.
  * Za različne načine poganjanja (razvoj/produkcija/...) imamo lahko različne nastavitve!
* Nekaj pomembnih spremenljivk:
  - `SECRET_KEY`: ključ za piškotke
  - `INSTALLED_APPS`: aplikacije v uporabi, tako uporabniške kot vgrajene (`django.contrib.*`)
  - `DATABASES`: podatkovne baze, ki jih uporablja projekt
  - `TIME_ZONE`: časovna cona

---

# Podatkovni model - `models.py`

* Vsak entitetni tip predstavimo z razredom, ki deduje od `django.db.models.Model`.
* Atribute predstavimo z razrednimi spremenljivkami ustreznega [tipa](https://docs.djangoproject.com/en/6.0/ref/models/fields/#model-field-types) (iz `django.db.models`):
  - `CharField`, `TextField`: tekstovni atributi
  - `IntegerField` ipd.: celoštevilski atributi
  - `DecimalField`, `FloatField`: decimalna števila
  - `DateField`, `DateTimeField`, `TimeField`: časovni atributi
  - `ForeignKey`: odnosi ena na več
  - `ManyToManyField`: odnosi več na več
* Razredom lahko določimo poljubne metode.

---

# Migracije

* Migracije skrbijo za spremembe podatkovne baze glede na spremembe modela.
* Po spremembi modela migracije ustvarimo z
  ```bash
  python manage.py makemigrations
  ```
* Migracije uveljavimo z
  ```bash
  python manage.py migrate
  ```
  - Ob prvem zagonu tako ustvarimo bazo!

---

# Skrbniški vmesnik

* Django ima že vgrajen skrbniški vmesnik.
* Uporabniški račun za skrbnika ustvarimo z
  ```bash
  python manage.py createsuperuser
  ```
* Poženimo razvojni strežnik:
  ```bash
  python manage.py runserver
  ```
* Do skrbniškega vmesnika lahko dostopamo na naslovu http://127.0.0.1:8000/admin/.
  - Prijavimo se s prej ustvarjenim uporabniškim imenom in geslom.

---

# Pogledi in poti

* Poglede definiramo s funkcijami v `views.py`.
  * Vsaka funkcija kot prvi argument `request` sprejme zahtevek, ki ga sprejme aplikacija.
  * Funkcije vračajo objekt tipa `django.http.HttpResponse` ali ustrezno dejanje (napaka, preusmeritev).
* V `urls.py` določimo poti in zanje ustrezne poglede.
  * Poti so lahko parametrizirane - parametri se podajo kot poimenovani parametri ustrezni funkciji.

---

# Predloge

* Predloge v obliki HTML postavimo v mapo `templates` znotraj mape aplikacije.
* Za prikaz predloge vrnemo rezultat funkcije `django.shortcuts.render`, ki ji podamo:
  - objekt `request`,
  - ime predloge (pot do datoteke znotraj mape `templates`), in
  - slovar z vrednostmi spremenljivk.
* V predlogah lahko uporabljamo sledečo sintakso:
  - `{{ spremenljivka }}`: vrednost spremenljivke
  - `{% značka argument ... %}`: [značka](https://docs.djangoproject.com/en/6.0/ref/templates/builtins/#ref-templates-builtins-tags) z ustrezno funkcionalnostjo

---

# Dedovanje predlog

* V osnovni predlogi (npr. `osnova.html`) lahko znotraj strukture spletne strani definiramo bloke:
  ```jinja
  {% block ime_bloka %}
  ...
  {% endblock %}
  ```
* V drugih predlogah lahko uporabimo značko `{% extends "osnova.html" %}` in na isti način znova definiramo (samo) bloke.
  * Vsebine blokov nadomestijo istoimenske bloke v osnovni predlogi.
  * Za bloke iz osnovne predloge, ki jih nismo definirali, vsebina ostane nespremenjena.

---

# Poti v predlogah

* Med razvojem aplikacije morda še ne poznamo točnega naslova, kjer bo tekla aplikacija.
  * Ali pa se lahko to naknadno spremeni!
* Dobra praksa je, da v predlogah poti ne navajamo ročno, pač pa zanje uporabimo značko `{% url %}`:
  ```jinja
  {% url "ime_poti" argument ... %}
  {% url "ime_poti" par1=arg1 ... %}
  ```
  * `"ime_poti"` je ime, podano s parametrom `name` pri določitvi poti s funkcijo `django.urls.path`
  * Dodatni argumenti (vsi poimenovani ali nepoimenovani) se vstavijo v pot.

---

# Objekti

* Na podlagi definiranih modelov lahko ustvarimo ustrezne objekte:
  ```python
  chuck = Oseba(ime="Chuck Norris")
  ```
* Do objektov v bazi lahko dostopamo preko "upravnika" (*manager*) `Model.objects`:
  ```python
  Oseba.objects.all() # vse osebe
  Zanr.objects.get(pk=1) # žanr z ID-jem 1

  # filmi iz leta 2000, urejeni padajoče po oceni
  Film.objects.filter(leto=2000).order_by("-ocena")

  # glavne vloge v filmih, dolgih vsaj 200 minut, ki nimajo oznake PG-13
  Vloga.objects.filter(film__dolzina__gte=200, mesto=1).exclude(film__oznaka='PG-13')
  ```
  * Dejanske poizvedbe se zgodijo šele takrat, ko potrebujemo podatke.

---

# Združevanje in grupiranje

* Z metodo `aggregate` lahko uporabimo eno ali več združevalnih funkcij na objektih v bazi:
  ```python
  from django.db.models import Avg, Count, Max, Min, Sum
  Film.objects.aggregate(Max("dolzina"), zasluzek=Sum("zasluzek"))
  # {'zasluzek': 279926080502, 'dolzina__max': 450}
  ```
* Če želimo grupirati po objektih nekega modela, uporabimo metodo `annotate`:
  ```python
  q = Film.objects.annotate(Count("zanri"))
  q[0].zanri__count
  ```

---

# Kontrola prebranih atributov

<span class="small">

* Z metodama `only` in `defer` poskrbimo, da iz baze preberemo samo podane atribute, oziroma podanih atributov ne preberemo:
  ```python
  Film.objects.only("dolzina", "leto").get(naslov="Jurski park")
  Film.objects.defer("opis").get(naslov="Jurski svet")
  ```
  * Če dostopamo do atributov, ki jih nismo prebrali, se bo naredila nova poizvedba!
* Metoda `select_related` poskrbi, da se preberejo tudi objekti, na katere se sklicuje navedeni tuji ključ.
  ```python
  Film.objects.filter(naslov__startswith="Jurski").select_related("oznaka")
  ```
* Metoda `prefetch_related` poskrbi, da se preberejo tudi objekti, povezani z navedenim odnosom več na več.
  ```python
  Film.objects.filter(naslov__startswith="Jurski").prefetch_related("vloge")
  ```

</span>

---

# Zahtevnejše poizvedbe

* Z razredoma `django.db.models.F` in `django.db.models.Q` lahko sestavljamo izraze, ki predstavljajo stolpce oziroma pogoje.
  ```python
  from django.db.models import F, Q

  # Filmi, ki so zaslužili vsaj 100 mio dolarjev na oceno
  # ali vsaj 5 mio dolarjev na minuto trajanja
  Film.objects.annotate(
    zasluzek_na_oceno=(F("zasluzek") / F("ocena")),
    zasluzek_na_dolzino=(F("zasluzek") / F("dolzina"))
  ).filter(
    Q(zasluzek_na_oceno__gt=100_000_000) |
    Q(zasluzek_na_dolzino__gt=5_000_000)
  )
  ```

---

# Spreminjanje objektov

* Objektom lahko spreminjamo polja kot običajno:
  ```python
  chuck.ime = 'Chuck Norris (RIP)'
  ```
* Spremembe so lahko odvisne tudi od trenutnih podatkov v bazi (tudi, če jih nismo še prebrali):
  ```python
  film.ocena = F('ocena') + 1
  ```
* Spremembo v bazo zapišemo z metodo `save`.
  ```python
  chuck.save()
  film.save()
  ```

---

# Transakcije

* Če ne določimo drugače, bo vsaka sprememba v bazi v svoji transakciji.
* Lahko določimo, da se neko zaporedje ukazov izvede znotraj ene transakcije:
  ```python
  from django.db import transaction

  with transaction.atomic():
      # ukazi, ki naj tvorijo transakcijo
  ```
* Kot transakcijo lahko določimo tudi celotno funkcijo:
  ```python
  @transaction.atomic
  def pogled(request, ...):
      ...
  ```
* POZOR: preklic transakcije (npr. ob napaki) ponastavi stanje v bazi, ne pa tudi v objektih!

---

# Avtentikacija

* Django ima že vgrajeno podporo za avtentikacijo, ki jo lahko vključimo med poti, npr.
  ```python
  path("accounts/", include("django.contrib.auth.urls")),
  ```
* Podprti so sledeči pogledi:
  - `login`: prijava
  - `logout`: odjava
  - `password_change`: menjava gesla
  - `password_reset`: ponastavitev gesla
* Za ustrezno uporabo je potrebna dodatna konfiguracija!

---

# Prijava in odjava

* Za prijavno stran je potrebno pripraviti predlogo `registration/login.html`.
* Ta mora vsebovati obrazec, ki z metodo `POST` pošlje podatke na pogled `login`, in vsebuje:
  - `{% csrf_token %}`,
  - polje za uporabniško ime z imenom `{{ form.username.html_name }}`
  - polje za geslo z imenom `{{ form.password.html_name }}`, ter
  - skrito polje `next` z vrednostjo `{{ next }}`.
* Za odjavo pošljemo obrazec z metodo `POST` na pogled `logout`.

---

# Registracija

* Za registracijo moramo poskrbeti sami.
* Pomagamo si lahko z obrazcem `django.contrib.auth.forms.UserCreationForm`.
  * Obrazec ustvarimo iz objekta `request.POST`, ali pa brez argumentov za prazen obrazec.
  * Obrazec vsebuje polja `username`, `password1` in `password2`.
  * Z metodo `is_valid` preverimo, ali so vpisani podatki veljavni.
  * Z metodo `save` shranimo obrazec in tako ustvarimo uporabnika.
  * Obrazec podamo v kontekstu, da lahko do njega v predlogi dostopamo preko spremenljivke `form`.

---

# Uporabniki in pravice

<span class="small">

* V pogledih lahko do uporabnika dostopamo preko objekta `request.user`.
* V predlogah lahko do uporabnika dostopamo preko spremenljivke `user`, npr.
  ```jinja
  {% if user.authenticated %}
  Pozdravljen, {{ user.username }}!
  {% endif %}
  ```
* Vsak model ima privzeto določene pravice `add`, `change`, `delete`, `view`, ki jih lahko dodeljujemo uporabnikom.
* Preko `request.user.has_perm` lahko preverimo, ali ima trenutni uporabnik ustrezne pravice:
  ```python
  if request.user.has_perm('app.add_model'):
      ...
  ```
* V predlogah lahko uporabimo spremenljivko `perms`:
  ```jinja
  {% if perms.app.add_model %}
  <!-- uporabnik lahko dodaja objekte za dani model -->
  {% endif %}
  ```

</span>

<span class="hidden">{% endraw %}</span>
