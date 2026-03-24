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

# 4. Vaje

## Popravek iz 3. vaj
Namesto `FloatField` je pri nas za oceno filma primerneje uporabljati `DecimalField`, ki ustreza Pythonovem `Decimal` objektu. Ta objekt lahko omejimo npr. na 3 števke z 1 decimalko, kar je ravno format ocen, ki ga želimo. (hvala za popravek Janoš!).

## Dodajanje več-na-več (many-to-many) relacij

Na 4. vajah smo najprej dodali še modele za odnose (več-na-več relacije).

Django zna sam ustvariti povezovalne tabele, kar povemo tako, da enemu izmed povezanih modelov dodamo `models.ManyToMany` polje.

Konkretneje, modelu za `Film` smo dodali `models.ManyToMany` polje `zanri`, ki sprejme razred `Zanr` (navada je, da je ime polja kar ime modela v množini).

Če s pomočjo npr. sqlite3 zdaj (po migraciji, seveda) pogledamo bazo, opazimo, da je Django naredil povezovalno tabelo.

Django ustvari povezovalno tabelo, če `ManyToMany` dodamo v enega izmed povezanih objektov (kateregakoli, a ne v oba). Ponavadi dodamo to polje v objekt, kjer je to smiselneje - Iz praktičnih vidikov je smiselneje, da bomo, npr. pri vnosu (na skrbniški nadzorni plošči ali drugje) uporabnika vprašali naj našteje žanre filma, ko bo dodajal film. Čudno bi bilo, če bi moral uporabnik pri dodajanju žanra našteti vse filme!


Odnos `Vloga` je nekoliko kompleksnejši, saj ima ta še dodatne stolpce. V takih primerih naredimo nov razred `Vloga`, kjer natančeneje opišemo kako izgleda povezovalna tabela in jo uporabimo tako, da v `models.ManyToMany` field, dodamo drugi argument `through=`. V našem primeru smo v model `Film` dodali `models.ManyToMany` polje na model `Oseba`, povezan preko `through=Vloga`.

Ob priliki smo spoznali še nekaj novosti:
- Polja lahko sprejmejo tudi argument `choices=`, ki omeji možne vrednosti. Možne vrednosti lahko podamo na več načinov, npr. kot seznam parov ali pa slovar...
- V `Meta` gnezdeni class lahko dodamo `models.UniqueConstraint`, ki pove kateri stolpci v tabeli morajo skupaj biti enolični (`UNIQUE` keyword v SQL)

## Uvoz modelov iz .csv datotek

Zdaj, ko imamo vse modele jih populirajmo kar z istimi `.csv` datotekami kot na predavanjih.
V ta namen smo ustvarili skripto `napolni_bazo.py`, kjer lahko vidimo, kako v Djangu interagiramo z bazo (glej skripto in komentarje v njej).

Vsakemu modelu pripada `Manager`, do katerega dostopamo z npr. `Oseba.objects`
S pomočjo le-tega lahko enostavno interagiramo z podatkovno bazo.

Nekaj primerov:
- Z `Oseba.objects.all()` lahko iteriramo skozi vse objekte v bazi, ki pripadajo `Oseba`.
- Z `Oseba.object.bulk_create(arg)` lahko iz seznama (ali podobno) `arg` objektov `Oseba` populiramo bazo.
- Z `Oseba.object.get(..)` lahko dobimo določen objekt iz baze. Napaka, če elementa ni v bazi, oz. če jih več ustreza argumentom
- Z `Oseba.object.get_or_create(..)` naredimo isto kot pri zgornji metodi, le da se objekt zgradi (in shrani v bazo) v kolikor, ga ni v bazi.
- Z `Oseba.objects.in_bulk()` dobimo slovar, kjer so ključi primarni ključi osebe, vrednosti pa pripadajoči objekti.

Vse bomo po potrebi našli v [dokumentaciji](https://docs.djangoproject.com/en/6.0/ref/models/querysets/)

Paket `django.db` vsebuje `transaction` s pomočjo česar lahko več interakcij z bazo zapakiramo v eno atomično transakcijo.

Pri nas je to lahko koristno iz vidika učinkovitosti (privzeto je vsak Django klic, ki interagira z bazo, npr. `save()` ena transakcija)

iz Podatkovnih Baz 1 pa vemo, da so transakcije koristne tudi kot način za garantiranje [ACID](https://en.wikipedia.org/wiki/ACID) lastnosti, ki so v praksi zelo pomembne.

Funkcijo `napolni_bazo.py` kličemo kar iz Django shell-a (`python manage.py shell`), kjer najprej uvozimo modul (našo skripto), npr.
`from filmapp.napolni_bazo import main` in potem `main()`.

# 5. Vaje

## Novi pogled - prikaži informacije o danem filmu

### Pogled z dodatnimi argumenti

Na vajah smo naredili resnejši pogled, ki prikazuje informacije, shranjene na podatkovni bazi.
Ta pogled bo poleg obveznega `request` parametra sprejel še drugi parameter `film_id` in prikazal informacije za dotičen film.
V njem s pomočjo `Film.objects.get(id=film_id)` pridobimo informacijo o dotičnem filmu, ki jo potem lahko prikažemo (recimo, spet z `HttpResponse` kot v našem prvem, testnem pogledu).
Kako pa bomo dostopali do tega pogleda? Številka `film_id` bo del url-ja. To lahko dosežemo tako, da v `urls.py` v path dodamo nekaj takega kot `film/<int:film_id>`. To pomeni, da na tem mestu v URL-ju pričakujemo število (int). To število bo drugi argument v našem pogledu.
Če sedaj gremo na našo aplikacijo in na koncu url-ja dodamo npr. `filmi/film/4972`, se bo prikazal primeren pogled (saj obstaja film s tem id-jem)

### 404 error

Če poskusimo priti na `filmi/film/1` bomo videli napako, saj v naši bazi ni filma s tem id-jem. V takih primerih bi bilo dobro sprožiti neko smiselno napako.
Vemo, da ima http nekaj uveljavjlenih [kod za napake](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes). V našem primeru bi bilo dobro sprožiti napako 404 - page not found.
To bi lahko storili tako, da `Film.objects.get(id=film_id)` zapakiramo v `try ... except ...` block, kjer raisamo primerno napako (V djangu obstaja 404 exception), vendar je ta situacija ("Poišči nekaj v bazi in vrži napako 404, če ta ne obstaja") tako pogosta, da v Djangu obstaja bližnjica `get_object_or_404`, ki se nahaja v paketu `django.shortcuts`.
Uporabimo jo kot

`film = get_object_or_404(Film, id=film_id)`

Če bo poizvedba uspešna se rezultat shrani v spremenljivko film, sicer pa se sproži napaka 404 (v Django pogledih se mora vedno vrniti primeren HttpResponse ali pa sprožiti napako).

Če zdaj ponovno gremo na `filmi/film/1` bomo opazili 404 error. Sicer vseeno ni podoben takšnemu kot smo jih vajeni iz vsakdanjega življenja - razlog je, da je v naših `settings.py` projekta nastavjlen `DEBUG = True`, zaradi česar tudi 404 error page poda nekaj dodatne informacije. Če začasno spremenimo na `DEBUG = False` opazimo kompaktnejši 404 error.

### Predloge

Morda se spomnimo, da smo za naš prvi testni pogled morali posebej uvozit `HttpResponse`. Django je privzeto za nas "pripravil" le funkcijo `render`, ki je še nismo uporabili.
Razlog je enostaven - v praksi se za prikazovanje pogledov uporablja `render` (ki vrača `HttpResponse`) in ne sam `HttpResponse`. S pomočjo funkcije `render` lahko razne podatke (npr. o filmu) pošljemo predlogi (template), ki predstavlja nekakšno ogrodje v HTML-ju, ki se bo populirali s poslanimi podatki.

V naši aplikaciji ustvarimo novo mapo `templates`, v kateri bodo shranjene naše predloge. Za preprečevanje konfliktov (v primeru, da bi imeli več predlog z istim imenom, kar se lahko zgodi pri večjih projektih), v mapi `templates` ustvarimo podmapo `filmiapp` v njo pa `film_podrobnosti.html`, kar bo naša predloga za ta pogled.

Najprej pomislimo kakšne informacije bomo iz pogleda poslali predlogi. Funkcijo `render` uporabimo na naslednji način:

`return render(request, 'filmiapp/film_podrobnosti.html', kontekst)`

Prvi argument je request (kar je tudi prvi argument pogleda), drugi argument je naša predloga, tretji pa je kontekst - Python slovar, ki vsebuje dodatne podatke s katerimi hočemo populirati predlogo. V našem primeru bo kontekst pod ključem "film" imel niz reprezentacijo filma (ki smo jo že definirali), pod ključem "podrobnosti" pa seznam parov (verbose ime polja, vrednost polja).

Predlogo pa pišemo kot ponavadi HTML, le da imamo na voljo nekatere značke, o katerih ste govorili že na predavanjih.
Tu smo uporabili:
- Značko `{{ ime_spremenljivke }}`, ki izpiše vrednost dane spremenljivke (v našem primeru v naslovu izpiše ime filma).
- Značko `{ % for ... in ... % }`, ki predstavlja zankanje (pri nas čez polja Film-a). Ker za razliko od Pythona nimamo identacije, moramo zanko zaključiti z `{% endfor %}`.

## Dodaten pogled - poišči najbolje ocenjenih X filmov

Naredimo še pogled, ki bo izpisal najboljse ocenjene filme. Spet torej dodamo novo funkcijo v `views.py` ter pripadajoč url v `urls.py`. 
Pogled spet sprejme številski argument - `st_najboljsih`, ki nam pove koliko najboljših filmov bomo prikazali.
S pomočjo objects Managerja lahko najboljše dobimo kot

`Film.objects.order_by('-ocena')[:st_najboljsih]`

`order_by` vrne filme, urejene po danem polju (stolpcu). Privzeto so urejeni naraščujoče, zato dodamo pred ime `-`, da bodo padajoče (DESC v SQL).
Na koncu izberemo le prvih `st_najboljsih` (LIMIT v SQL). Potrebne podatke potem spet shranimo v slovar (kontekst) in z `render()` to passamo v novo predlogo.

V predlogi `filmiapp/film_podrobnosti.html` prikažemo seznam (ordered list v HTML) najboljših nekaj filmov.
Posamezen element seznama je imel na začetku obliko:
`<li><a href="/filmi/film/{{id}}">{{naslov}}</a>: {{ocena}}</li>`

Ideja je, da lahko na naslov filma kliknemo, kar nas vrže na primerno stran, ki prikaže dodatne informacije o danem filmu.
Tak pristop krši [DRY](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself) princip programiranja - isto informacijo (url) imamo zdaj na dveh mestih. V naši predlogi ter v `urls.py`. To zlahka vodi do napak, če bomo npr. enkrat spremenili url v `urls.py`, ampak pozabili spremeniti v predlogi (oziroma mogoče celo v več predlogah...)

To lahko rešimo z `{% url ... %}` značko, ki ji damo ime poti iz `urls.py`:

`<li><a href="{% url 'film_podrobnosti' id %}">{{naslov}}</a>: {{ocena}}</li>`

Podobno kot pri predlogah, smo lahko v težavah pri večjih projektih, saj morda več aplikacij uporablja isto ime za razne poti.
V tem primeru lahko dodamo namespacing našim potem (eksplicitno povemo še iz katere aplikacije jemljemo določeno pot).

Zgornji element seznama tako postane:

`<li><a href="{% url 'filmiapp:film_podrobnosti' id %}">{{naslov}}</a>: {{ocena}}</li>`


