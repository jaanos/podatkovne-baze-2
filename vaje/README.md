# 2. Vaje

Na 2. vajah smo naredili Django projekt in si pogledali nekaj osnov Django-ta

## Django - hiter pregled projekta

Django projekt preprosto naredimo z ukazom\
`django-admin startproject "ime_projekta" "ime_mape"`

Torej, `django-admin startproject filmi filmi_projekt` bo ustvaril mapo "filmi_projekt" v kateri se nahaja naš projekt "filmi".\
V mapi "filmi_projekt" opazimo datoteko *manage.py* s pomočjo katere lahko upravljamo s projektom.\
Npr. če poženemo `python manage.py runserver` se lokalno požene testna spletna stran. Tekom predmeta bomo to stran spreminjali.\
Če pa poženemo `python manage.py createsuperuser` lahko naredimo skrbniški račun (več o tem pozneje).

V mapi "filmi" (ime projekta) je Django za nas že ustvaril nekaj datotek:
- datoteka `__init__.py` predstavlja, da je "filmi" Pythonov [package](https://docs.python.org/3/tutorial/modules.html#packages) in jo pustimo pri miru.
- datoteki `asgi.py` in `wsgi.py` se nanašata na deployment projekta.
- v datoteki `settings.py` se nahajajo razne nastavitve projekta. Med drugim je pomemben seznam aplikacij (*INSTALLED_APPS*). Poleg privzetih bomo tu dodajali še svojo aplikacijo - vsak Django projekt je namreč sestavljen iz več aplikacij.
- v datoteko `urls.py` bomo dodajali url-je (npr. do aplikacij). Zaenkrat imamo že url do skrbniške nadzorne plošče (do katere lahko že dostopamo).

## Django - naredimo aplikacijo

Kot rečeno je Django sestavljen iz aplikacij. Pa dodajmo aplikacijo *filmiapp*:\
`python manage.py startapp filmiapp`\
S tem je Django ustvari mapo *filmiapp* v kateri bo naša aplikacija. Spet je Django za nas že ustvaril nekaj skript:
- `__init__.py` označuje, da je tudi *filmiapp* Python package.
- `admin.py` nam bo omogočal, da aplikacijo dodamo na skrbniško nadzorno ploščo (pozneje).
- v `models.py` bomo definirali modele (podobno kot ORM, ki ga trenutno sestavljate na predavanjih)
- v `tests.py` bomo morda pozneje napisali teste aplikacij.
- v `views.py` bomo dodali razne poglede (npr. HTML).
- S pomočjo `apps.py` se lahko trenutno sklicujemo na aplikacijo (kmalu bomo videli kako)

## Django - primer: dodajanje pogleda

V `views.py` smo s pomočjo djangotovega `HttpResponse` dodali pogled `test`.\
Da bomo do njega lahko dostopali mu moramo določiti še url. V ta namen v mapo *filmiapp*
dodajmo `urls.py`.\
`urls.py` izgleda podobno kot datoteka z istim imenom v mapi `filmi`, kjer definiramo, da bo viewu *test* ustrezal URL "".\
"" je naslov našega viewa znotraj aplikacije *filmiapp*, ta aplikacija pa trenutno še ni povezana z našim projektom *filmi*, povežemo ju tako, da aplikacijo dodamo še v `urls.py` v mapi *filmi*. Aplikacije vežemo s pomočjo funkcije `include`.\
Če spet poženemo stran (`python manage.py runserver`) vidimo, da ta ne dela več - prejšnja testna stran se pokaže le, če nismo definirali nobenih svojih aplikacij. Če na koncu URL-ja dodamo "filmi/" (kar je ravno naslov našega viewa), bi morali videti izpisan naš pogled: "To je test".

## Django - Ustvarjanje modelov

Ustvarimo še nekaj modelov v `models.py` v mapi *filmiapp*.\
Modele predstavimo z razredi, ki dedujejo od `models.Model`.\
Na voljo imamo veliko [atributov](https://docs.djangoproject.com/en/6.0/topics/db/models/), ki bodo ustrezali stolpcem v podatkovni bazi (spet, ORM). Modeloma Oznaka in Oseba bomo dodali CharField.\
Če želimo ustvariti shemo podatkovne baze, ki ustreza modelom, moramo našo aplikacijo najprej dodati v seznam `INSTALLED_APPS` v datoteki `settings.py` našega projekta.\
Django-tov "vmesnik" med našimi modeli in dejansko podatkovno bazo so [migracije](https://docs.djangoproject.com/en/6.0/topics/migrations/).\
Migracije za aplikacijo *filmiapp* pripravimo z ukazom:\
`python manage.py makemigrations filmiapp`.
Vse pripravljene migracije potem apliciramo (ustvarimo/spremenimo bazo) z ukazom:\
`python manage.py migrate`.\
Pri tem opazimo, da je Django migriral še ostale modele, ki so bili privzeti nastavljeni (ostale aplikacije v `INSTALLED_APPS`).\
S pomočjo ukaza:
`python manage.py sqlmigrate filmiapp 0001`
(0001 je številka migracije, kar lahko preberemo ob migraciji) lahko vidimo še SQL, ki se je v ozadju izvedel. Med drugim vidimo, npr., da je Django vsakemu modelu avtomatsko dodal ključ id.
Opazimo še, da je v našem projektu zdaj prisotna še datoteka `db.sqlite3` (RDBMS bomo pozneje spremenili v `settings.py` iz sqlite3 na nekaj resnejšega).


## Django - "igranje z bazo"

Če poženemo `python manage.py shell` vstopimo v Pythonov shell, kjer lahko stestiramo Djangotov ORM.\
Ustvarimo lahko npr. objekte iz naših modelov in jih shranjujemo v podatkovno bazo.
Nekaj primerov je [tu](https://docs.djangoproject.com/en/6.0/topics/db/models/).\
Dobra praksa je še, da vsakemu modelu dodamo še `__str__` metodo, s katero dobimo lepši izpis.\
\
Poleg shell-a lahko do baze dostopamo tudi s pomočjo skrbniške nadzorne plošče.
V ta namen moramo naše modele dodati v `admin.py` datoteko v naši aplikaciji.

# 3. Vaje

Na 3. vajah smo v `models.py` dodali vse modele, ki ste jih imeli na predavanjih.
Pri tem smo si na veliko pomagali z referenco o različnih možnosti za [polja](https://docs.djangoproject.com/en/6.0/ref/models/fields/#model-field-types),
na primer:
- `models.CharField()` smo že opazili, ustreza `VARCHAR` v SQL (nujno je treba dati še argument `max_length`),
- `models.IntegerField()` ustreža celemu številu (integer), dovoljene vrednosti so vsaj do +-2*10^9,
- `models.FloatField()` predstavlja decimalno (floating point) število,
- `models.PositiveIntegerField()` ustreza naravnemu številu (do vsaj ~2*10^9), tehnično je dovoljena tudi vrednost `0` (ampak se ji raje izognemo - kot vidimo v dokumentaciji je to zgolj zaradi "backwards compatibility" razlogov)
- `models.PositiveSmallIntegerField()` ustreza naravnemu število do vsaj ~3*10^4, spet je dovojlena tudi vrednost `0`.
- `models.ForeignKey` referenca na ključ kakšne druge tabele, torej many-to-one relacija. Nujna argumenta sta Class na katerega se referenciramo ter `on_delete`. Avtomatsko se naredi tudi index na tem stolpcu (kar seveda lahko tudi disable-amo).

Ti fieldi imajo lahko tudi argumente:
- `null`: privzeto je `False`, kar ustreza `NOT NULL` v SQL.
- `blank`: privzeto je `False`, kar pomeni, da je ob vnosu (v formah ali na skrbniški nadzorni plošči), ta podatek obvezno vnesti.
- `default` - privzeta vrednost za to polje.
- `editable` - privzeto je `True`, kar pomeni, da lahko to polje ročno popravimo npr. na skrbniški nadzorni plošči.
- `help_text` - text, ki se pojavi kot pomoč, npr. pri vnosu tega polja
- `verbose_name` - podrobneje ime polja, ki se izpiše npr. pri formah ali na skrbniški nadzorni plošči (privzeto se izpiše kar ime atributa)
- `primary_key` - `True`, če želimo, da je dotično polje primary key. Če tega ne nastavimo, Django avtomatsko naredi primary-key `id` za nas.
- `unique` - privzeto je `False`, kar pomeni, da vrednosti niso nujno enolične.
- `on_delete` - relevantno za `ForeignKey`, pove kaj se zgodi, če zbrišemo objekt na katerega se `ForeignKey` nanaša.

Kot prej ima vsak model tudi svoj `__str__`, kjer včasih vrnemo f-nize (saj morda ne vračamo vedno le CharFielda in je treba atribut najprej pretvoriti v niz).

Modeli iz predavanj, ki jih nismo dodali v Django `models.py`:\
- `Uporabnik`, saj je Django že sam avtomatsko ustvaril ta model (kot smo videli v skrbniški nadzorni plošči).
- `Vloga` in `Pripada`, saj so to povezovalne table (many-to-many), katere lahko v Django boljše naredimo, kar bomo videli kasneje.

Ko končamo, dodamo vse nove modele še v `admin.py` ter spet poženemo `makemigrations` ter `migrate` in nove tabele bi morale biti
vidne v skrbniški nadzorni plošči, kjer lahko že dodajamo in spreminjamo podatke.

## meta podatki

V naše modele lahko dodamo še meta [podatke](https://docs.djangoproject.com/en/6.0/topics/db/models/#meta-options).
To naredimo s tem, da dodamo vgnezden `class Meta`.
V `Meta` razred lahko npr. dodamo ordering, ki določa v katerem vrstnem redu se bodo vrstice prikazovale.
Definiramo lahko tudi kako se prikazuje ime modela v množini, torej končno imamo lahko "Osebe" in "Filmi" v skrbniški nadzorni plošči, namesto "Osebas" in "Films".

