---
marp: true
style: "@import url('style.css')"
---

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