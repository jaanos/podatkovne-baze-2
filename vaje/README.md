{% raw %}
# Navodila za prvo pripravo projekta iz nule

Za projekt potrebujemo Django (`pip install django`).
Po svežem kloniranju tega repozitorija, lahko stran pripravimo s sledečimi ukazi:
- premaknemo se v mapo `filmi_projekt`.
- Pripravimo podatkovno bazo `python manage.py migrate`
- Podatkovno bazo napolnimo z:
    - `python manage.py shell`
    - `from filmiapp.napolni_bazo import main(); main()`
    - z `python manage.py createsuperuser` si naredimo admin račun.
- `python manage.py runserver` bi zdaj moral delati.

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
- Značko `{% for ... in ... %}` (brez navednic), ki predstavlja zankanje (pri nas čez polja Film-a). Ker za razliko od Pythona nimamo identacije, moramo zanko zaključiti z `{% endfor %}` (brez navednic).

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

To lahko rešimo z `{% url ... %}` značko (brez navednic), ki ji damo ime poti iz `urls.py`:

`<li><a href="{% url 'film_podrobnosti' id %}">{{naslov}}</a>: {{ocena}}</li>`

Podobno kot pri predlogah, smo lahko v težavah pri večjih projektih, saj morda več aplikacij uporablja isto ime za razne poti.
V tem primeru lahko dodamo namespacing našim potem (eksplicitno povemo še iz katere aplikacije jemljemo določeno pot).

Zgornji element seznama tako postane:

`<li><a href="{% url 'filmiapp:film_podrobnosti' id %}">{{naslov}}</a>: {{ocena}}</li>`

# Predavanja med 5. in 6. vajami

## Dedovanje predlog

Na predavanjih so bile naše predloge iz vaj izboljšane. In sicer, skupni HTML, ki se ves čas ponavlja je bil premaknjen v `osnova.html`, v katerem s pomočjo `{% block ime_bloka %}` in `{% endblock %}` značk definiramo bloke kode, ki jih lahko v ostalih predlogah prepišemo. Dodatno je bil HTML močno izboljšan s pomočjo [Bulma CSS](https://bulma.io/)\

V naših predlogah od prej, npr. `podrobnosti.html` potem najprej označimo, da dedujemo iz `osnova.html` z `{% extends osnovna_predloga %}` in definiramo kaj naj se pojavi v posameznih `{% block ime_bloka %}` značkah.

## Dodatne stvari v osnova.html

V nadaljevanju ste izkoristili funkcionalnosti aplikacij, ki so že v Django-tu (spomnimo se na `INSTALLED_APPS` v `settings.py`).
Med drugim ste link na "dodaj film" (ki zaenkrat še ne obstaja) skrili pod značko `{% if perms.filmiapp.add_film %}` - ta link lahko vidijo torej le uporabniki, ki imajo dovoljenje za dodajanje filma (npr. administratorji).
Z `{% if user.is_authenticated %}`, preverimo ali je uporabnim sploh prijavljen.
Podobno opazimo tudi `{% for message in messages %}`, ki spet uporablja eno izmed Djangotovih aplikacij za sporočila/opozorila (bomo še videli v praksi).


## Dodajanje prijave, odjave in registracije.

V `urls.py` ste dodali pot `accounts` do te aplikacije. To nam da dostop do login, password_change, password_reset in podobno.
Konkretno ste `login.html` dodali v `templates/registration`.
`login.html` spet razširi `osnova.html`, nova stvar je značka `{% block.super %}` s pomočjo katerih blokov ne prepišemo ampak jih le razširimo (če so bili morda že v osnovi neprazni).
Za samo prijavo uporabimo seveda HTML-jeve <form></form> značke s katerimo naredimo POST request, kjer je action enak poti z imenom `login`. Vnosna polja, ki morajo biti prisotna s določenimi imeni ste omenjali na predavanjih. Ne smemo pozabiti na `{% csrf_token %}`, ki mora biti vedno prisotna v primeru POST (sicer se Django pritoži) - ta značka izboljša [varnost naše strani](https://en.wikipedia.org/wiki/Cross-site_request_forgery).\

"Odjava" je le gumb (ki se prikaže le, če smo prijavljeni), ki pošlje POST request na pot z imenom logout.

Podobno ste naredili tudi predlogo za registracijo, kjer ste ročno dodali še primerni pogled. Tu ste uporabili funkcijo `redirect(ime)`, ki po POST requestu preusmeri uporabnika na pot z danim imenom - zelo pogosta praksa [post - redirect -get](https://en.wikipedia.org/wiki/Post/Redirect/Get).

# 6. Vaje

Na 6. vajah smo se še naprej lotevali obrazcev (angl. forms), kar ste sicer že delali na predavanjih.

## Iskanje želenega filma

Za začetek smo dodali stran, s pomočjo katere poiščemo poljuben film (zaenkrat jih lahko najdemo le preko seznama najboljših ali pa direkt preko id-ja, kar ni praktično).\

### pogled

Začnemo s tem, da naredimo nov pogled `film_poisci`, kjer najprej preberemo iskan film (ki bo GET request, saj ne spreminjamo ničesar na strežniku, ampak le pridobivamo podatke). To predstavlja vrstica
`poizvedba = request.GET.get('zacetek', '')`.\

`request.GET` je podoben Python-ovem slovarju in bi v resnici lahko poizvedbo dobili tudi kot indeksiranje z [], vendar je .get() metoda varnejša, saj lahko kot 2. argument podamo privzeto vrednost, v primeru da ključa `zacetek` (začetek filma) ni v slovarju.\

Če `zacetek` ni prazen, filme, ki mu ustrezajo dobimo preko Managerja z 
`Film.objects.filter(naslov__istartswith=poizvedba)[:100]`, ki vrne filme, ki se začnejo z nizom `poizvedba` (i pri `istartswith` pomeni, da nas ne zanimajo velike in male začetnice - čeprav pri naši trenutni konfiguraciji začetnice niso važne tudi, če uporabimo `naslov__startswith`). Da nimamo prevelikega seznama, smo število filmov omejili na 100 (rezultat je lahko ogromen, če bi npr. nekdo v iskalnik unesel samo "t").\

### Predloga

Filmi, ki ustrezajo poizvedbi, ter samo poizvedbo potem podamo kot kontekst in prikažemo `filmiapp/film_poisci.html` - to predlogo pa moramo še spisati, seveda bo spet dedovala iz `osnova.html` - dodatno bomo to pot še dodali na navbar v `osnova.html`.

Če je rezultat prisoten (`{% if poizvedba %}`), se zankamo čez filme in jih izpišemo, podobno kot v `film_najboljsi.html`.\

Nad tem bomo imeli obrazec `<form>`, ki pošlje GET request na dan (kar isti) pogled. V obrazcu imamo `<input>` tipa text z imenom `zacetek`, kar se bo poslalo v našem GET requestu. Ker ger za GET in ne POST request, `{% csrf_token %}` ni potreben. Spet smo uporabili podobne classe kot ste jih na predavanjih pri npr. `login.html`.

## Glasovanje za film

Dodali smo še funkcionalnost glasovanja za film. Če se spomnimo - glasovi so bili eni izmed polj od Film. Nekateri filmi jih že imajo, delamo pa se, da morda lahko uporabnik še dodatno glasuje za želene filme (zaenkrat dovolimo, da isti uporabnik glasuje večkrat).

### Spremembe v predlogi 

Gumb za glasovanje bomo dodali kar na `film_podrobnosti.html`. Pod podatke o filmu dodamo obrazec, ki ima tokrat `method="POST"` (saj spreminjamo podatke v podatkovni bazi) in pošlje informacije na `filmiapp:film_glasuj` (to pot bomo še naredili in povezali na primeren pogled). V obrazcu bo en sam gumb "Glasuj". Ker pa želimo podati še informacijo o id-ju filma, za katerega glasujemo, je prisoten še input element z tipom `hidden`, ki to informacijo posreduje (to ni edini način, nehigienično bi lahko id celo podali kot parameter v url-ju, kot smo to v naredili v `film_podrobnosti`). Seveda ne smemo pozabiti na `{% csrf_token %}`, saj gre za POST request.

### Pogled

V pogledu `film_glasuj` najprej preverimo, če je tip requesta res enak "POST". Če da, poskusimo dobiti film z danim id-jem in povečati število glasov za 1.
To storimo z
`film.glasovi = F('glasovi') + 1`
F (in Q) ste omenjali na predavanjih. V tem primeru je to priročen način za prebiranje in spreminjanje polja v enem samem stavku (zato tudi ne rabimo `atomic.transaction`).\

Da uporabniko jasno prikažemo, da je šlo vse v redu uporabimo še Djangotov messages za obvestila (kot prej omenjeno):
`messages.success(request, "Vaš glas je bil zabeležen!")`, kar bo povzročilo, da se prikaže zeleno ("success") obvestilo z danim tekstom.\

Na koncu kot prej uporabimo še `redirect`, da se vrnemo na pot z imenom `filmiapp:film_podrobnost` z film_id `film_id` (redirect zna avtomatsko ime poti takole povezati z integer parametrom, da se izognemo hardcode-anju poti).\

Kaj pa, če uporabnik nekako pride na to stran navadno (preko metode GET)? Tega seveda nočemo - ta pogled je samo za glasovanje. Na npr. [Wikipediji](https://en.wikipedia.org/wiki/List_of_HTTP_status_codeshttps://en.wikipedia.org/wiki/List_of_HTTP_status_codes) preverimo, da je v tem primeru pravilno vrniti kodo za napako 405. V Django-tu to pomeni, da enostavno vrnemo:
`return HttpResponseNotAllowed(['POST'])`, kjer so v argumentu le dovoljeni (v našem primeru POST) requesti.\

Za na konec - smiselno se zdi, da lahko le prijavljeni uporabniki glasujejo. To preprosto dosežemo tako, da nad naš pogled dodamo dekorator `@login_required`, ki seveda prav tako uporablja Djangotovo aplikacijo za avtentikacijo. Če sedaj pridemo na ta pogled in nismo prijavljeni, nas bo vrglo na stran za prijavo.

# 7. Vaje

## Dodatek form za Oseba

Na 7. Vajah smo za ponovitev vso mašinerijo (iskanje, dodajanje ipd.), ki jo imamo za filme, naredili še za osebe. V glavnem je zelo podobno (paziti moramo seveda pri npr. `filmiapp.perms.add_film`, ki postane npr. `filmiapp.perms.add_oseba`)

Kot ste na predavanjih s pomočjo `ModelForm` naredili ``FilmForm`, smo na vajah naredili še (sicer kar trivialno, saj je samo eno polje) `OsebaForm`.
V `Meta` moramo nujno povedati katera polja so vključena. Pri `FilmForm` smo enostavno rekli `exclude = ["vloge"]`, za katere smo se odločili, da jih ne bo, pri `OsebaForm` pa smo nasprotno povedali, kaj je vključeno: `fields = ["ime"]`. V tem primeru bi lahko rekli tudi `fields = '__all__'` (vse), vendar je varneje biti ekspliciten (morda bomo v prihodnje dodali še kaj polj).

## Preprečevanje večkratnega glasovanja

### Shranjevanje podatkov o glasovih 

Drugi del vaj smo posvetili izboljšanju našega sistema glasovanja. Zadnjič smo namreč videli, da lahko uporabnik poljubnokrat glasuje za dan film. Če hočemo to preprečiti, si moramo shraniti informacijo o filmih, o katerih je dan uporabnik že glasoval. V ta namen smo v `models.py` dodali nov model (torej, tabelo v podatkovni bazi) `DaniGlasovi`, ki imajo dve polji - tuj ključ na `Film`, ter tuj ključ na `User` (uporabnik - ta model je že v Django-tu in ga importamo). Dodatno smo z `Meta` dodali še vez enoličnosti (hočemo, da se vsaka kombinacija filma in uporabnika pojavi največ enkrat).

### Sprememba pogleda

Naš pogled `film_glasuj` je do zdaj ob prejemu POST requesta povečal število glasov za dan film. V novi verziji želimo, da se to zgodi, le če dan uporabnik še ni glasoval, sicer pa glas odvzamemo.

Ko dobimo POST request torej najprej izluščimo uporabnika z `request.user` in pokličemo že od prej znano:

`glas, ustvarjen = DaniGlasovi.objects.get_or_create(uporabnik=user, film=film)`,
ki vrne pripadajoč objekt `glas` (če je ta že v bazi, sicer ga pač ustvari). Spremenljivka `ustvarjen` je `True`, če je bil objekt na novo ustvarjen (kar pomeni, da še nismo glasovali za ta film).

Če smo za film že glasovali, POST request pomeni odvzem glasa, torej zmanjšamo število glasov danega filma (z `F` kot zadnjič) in zbrišemo `glas` iz podatkovne baze.

Če za film še nismo glasovali pa povečamo število glasov danega filma, pripadajoča vrstica v `DaniGlasovi` pa je itak že prisotna. V vsakem primeru pokličemo še `film.save()`. Ker imamo zdaj več operacij v tem pogledu, celoten pogled še ovijemo z `transaction.atomic` dekoratorjem.

### Sprememba gumba glasuj

Še zadnja sprememba se tiče predloge. Želimo, da se zelen gumb "glasuj" prikazuje le, če se nismo glasovali za film, sicer pa se prikaže rdeč gumb "odvzemi glas". To bomo naredili z značkami, kjer želimo značko tipa `{% if smo_glasovali %}`... Ker take značke ni, jo bomo [naredili](https://docs.djangoproject.com/en/6.0/howto/custom-template-tags/). V resnici bomo naredili "filter", kar lahko uporabljamo na podoben način kot značke (tags).

V naši aplikaciji dodamo mapo `templatetags` v kateri je `__init__.py` (spet označimo, da gre za package) in `filmiapp_extras.py`, kjer bomo definirali dodatne značke.
Dodatne značke, ki jih definiramo je treba registrirati. V ta namen mora biti v modulu nujno spremenljivka `register = template.Library()`.
Definiramo funkcijo `je_glasoval(uporabnik, film)`, ki bo vrnila `True`, če je dan uporabnik že glasoval za dan film, za kar uporabimo kar uporabimo kar `DaniGlasovi.objects.filter(uporabnik=uporabnik, film=film).exists()`, kar preverja zgolj obstoj vrstice v tabeli (bolj učinkovito kot npr. `.all()`). Sicer je ta način vseeno neučinkovit (Tabela DaniGlasovi je morda ogromna in polna filmov in uporabnikov, ki nas ne zanimajo) - naslednjič bomo pokazali boljši pristop.

 To funkcijo registriramo kar z dodajanjem dekoratorja `@register.filter`. Da bomo lahko to uporabili še v naši predlogi, moramo najprej na začetku predloge naše dodatne značke naložiti z:
`{% load filmiapp_extras %}`, glasovanje pa potem lahko preverimo z `{% if user|je_glasoval:film %}` (torej ime funkcije gre v sredino, argumenta pa na obe strani).

# 8. Vaje

## Splošni komentar iz 8. Vaj

## Boljši oseba_poisci pogled

Na vajah smo najprej posodobili naš pogled `oseba_poisci`, ki je prej poiskal vse osebe iz tabele `Oseba`, katerih ime se začne z dano poizvedbo.
Radi bi v iskane vključili tudi tiste, katerim se morda priimek začne z dano poizvedbo. Ima in priimek sta v naši bazi oba pod poljem `ime`, ločena s presledkom. Uporabiti je treba torej drugačni `.filter()`, morda tak, ki bi bil podoben `LIKE` v SQL.
Izkaže se, da lahko uporabljamo regularne izraze - [regex](https://en.wikipedia.org/wiki/Regular_expression), ki nam omogočajo, da definiramo vzorec in v rezultat vključimo vsa imena, ki ustrezajo danemu vzorcu. Na [internetu](https://stackoverflow.com/questions/525635/regular-expression-match-start-or-whitespace) hitro najdemo, da je primeren vzorec `'\\b' + poizvedba`, ki bo ustrezal vsakemu "koncu besede", za katerim je naša poizvedba, kjer kot "konec besede" lahko začetek besede, presledek (ravno to kar hočemo) oz. katerikoli znak ki ni alfanumeričen (kar je mogoče ok za npr. pomišljaj, ampak ne za apostrof).
V ta namen samo v filter namesto
`istartswith=poizvedba`
damo
`iregex='\\b'+poizvedba`

## Alternativno delovanje filtra je_glasoval

Zadnjič smo naredili filter `je_glasoval`, ki uporabi:
`DaniGlasovi.objects.filter(uporabnik=uporabnik, film=film).exists()`
Rekli smo, da je to sicer ok, ampak da bi morda bilo lepše, če bi lahko klicali kar nekaj takega kot `uporabnik_glasovi(film).exists()`, da nam npr. ni treba uvozit `DaniGlasovi`.

Čeprav nismo eksplicitno (za razliko od Vlog) dali `ManyToMany` polja v film, Django avtomatsko ve, da `DaniGlasovi` obstaja in
`film.daniglasovi_set` se nanaša na vse vrstice v `DaniGlasovi`, ki vsebujejo dani film.
Tako lahko zgornje nadomestimo z npr.
`film.daniglasovi_set.filter(uporabnik=uporabnik).exists()`
Ker je pa to nekoliko grdo (tale `_set`), lahko tudi definiramo svoja imena. To storimo tako, da v `ForeignKey` poljih v modelu za `DaniGlasovi` dodamo argument `related_name`.
Npr, če filmom v `DaniGlasovi` dodamo `related_name='obstojeci_glasovi`, bomo lahko uporabili kar `film.obstojeci_glasovi.filter(uporabnik=uporabnik).exists()` (ime je vseeno mogoče malo nerodno in morda bi bilo bolje, da bi v `Film` kar eksplicitno dodali `ManyToMany` field. Pri tem bi morali paziti, da tudi to pri `FilmForm` izključimo iz obrazca!)

`related_name` bi lahko uporabili tudi izven združevalnih tabel. Npr. v `Film` imamo `ManyToMany` polje `Vloge` s katerim lahko dostopamo do igralcev/režiserja v filmu. Kaj pa, če bi za dano osebo hoteli vedeti, v katerih filmih je sodeloval? V tem primeru, bi spet lahko uporabili `oseba.vloge_set...`, ali pa lepše ime, če bi `ManyToMany` polje v `Film` imelo `related_name`.

## Učinkovitejši filter je_glasoval

Prejšnje spremembe so v resnici v ozadju isti SQL in so torej bolj stvar okusa. Če bi hoteli, da `je_glasoval` deluje hitreje, bi morali uporabiti drugačen pristop. Najlažje je, da v tabelo `DaniGlasovi` na stolpca `film` in `uporabnik` (torej stolpca, po katerih nameravamo pogosto skupaj poizvedovati) dodamo [indeks](https://docs.djangoproject.com/en/6.0/ref/models/options/#indexes), o katerih ste govorili na predavanjih.
To storimo z `Meta` class-om, kjer dodamo spremenljivko `indexes = [models.Index(fields=['uporabnik', 'film'])]`. `indexes` je seznam različnih indeksov na tabeli, vsakega pa definiramo z `models.Index([...])`. S tem postanejo poizvedbe cenejše, vendar pa moramo biti pazljivi, saj z večjo količino indeksov raste kompleksnost npr. vstavljanja novih podatkov v tabelo.

## "Dolg od prej" - ocena v filmih

Ko smo delali model za `Film` smo dodali polje:
`ocena = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Ocena filma") # Omejimo to na [0,10]?`
Sedaj bomo razrešili še ta komentar, torej omejili možne ocene na interval [0, 10], saj je trenutno legalna cena tudi npr. 15 (lahko preverimo).
To v Django-tu naredimo z [validatorji](https://docs.djangoproject.com/en/6.0/ref/validators/). Konkretno, iz `django.core.validators` bomo uvozili `MinValueValidator` in `MaxValueValidator`.
Pri `ocena` pa v `models.DecimalField` dodajmo še argument:
`validators=[MinValueValidator(0, 'Ocena mora biti vsaj 0'), MaxValueValidator(10, 'Ocena je lahko največ 10')]`. Sedaj ni več mogoče npr. v obrazcu vnesti napačno oceno (ampak napačne ocene, ki so že v bazi bodo take tudi ostale!). Drugi argument teh validatorjev so tekst, ki se npr. v obrazcu izpiše, če pogoj prekršimo (privzeto je seveda v angleščini).

## "Dolg od prej" - null=True v filmih

V `Film` imamo tudi
`# Opis - pazi glede null vrednosti za charfield`
`opis = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Opis filma", help_text="Opis filma, do 1000 znakov")`

Komentar se nanaša na [opozorilo](https://docs.djangoproject.com/en/6.0/ref/models/fields/#null) v dokumentaciji, ki priporoča, naj se `null=True` ne uporablja za `CharField` in podobna (tekstovna) polja.

Namreč z `null=True` (NULL so dovoljeni) imamo pri tekstu dva različna načina, s katerimi povemo, da podatek manjka - NULL ali pa prazen niz `''`. To lahko povzroči težave, saj bomo morali npr. vedno paziti, ali polje manjka na oba načina (če bi kje pozabili in bi npr. preverjali samo za NULL (None), bi bile lahko težave, če je niz prazen).

Zato `null=True` odstranimo (privzeto je `False`). Ker pa še vedno nočemo, da je `opis` obvezen (`blank=True` samo pove, da v obrazcih ni potreben, v bazi ima v tabeli za filme še vedno nujno neko vrednost), dodamo še `default=''`. Privzeto je torej prazen.

## Uvod v Linux in terminal

Na koncu vaj smo začeli še z terminalom, kjer smo si pogledali nekaj zelo osnovnih ukazov, ki ste jih videli na predavanjih.
Omenil sem zelo enostavno berljiv [tutorial](https://ryanstutorials.net/linuxtutorial/), ki gre res skozi osnove, pogledali pa smo si tudi ukaz `ssh` (ki deluje tudi v Windows Powershell-u), s katerim se pogosto povežemo na oddaljene strežnike.
Povedali smo sintakso `ssh naslov_streznika -p stevilka_porta`. To nas poskuša povezati na streznik, kar z istim uporabniskim imenom, ki ga imamo lokalno na našem računalniku. `-p številka porta` je ponavadi odveč, saj je [standardno](https://en.wikipedia.org/wiki/Port_(computer_networking)), da se SSH dela preko porta 22, kar je tudi privzeta vrednost.
Pogosto se hočemo na strežnik prijaviti z alternativnim uporabniškim imenom, kar storimo z `ssh uporabnisko_ime@naslov_streznika`.


# 9. Vaje

Na 9. Vajah smo se večinoma spoznavali z web interface-om za PostgreSQL [PhpPgAdmin](http://baza.fmf.uni-lj.si/phppgadmin/), kjer smo videli tudi nekaj naprednih funkcionalnosti, ki jih ponuja PostgreSQL.

## Sprememba Django baze

Nato smo začeli pisati novo `settings.py` (ki bo uvozila staro in povozila `DATABASES` spremenljivko), kjer nameravamo spremeniti podatkovno bazo.
Kot piše v [dokumentaciji](https://docs.djangoproject.com/en/6.0/ref/databases/), bo treba za delo s sistemom PostgreSQL namestiti Python knjižnico `psycopg`.
Vidimo tudi, da bomo v slovarju `default` v slovarju `DATABASES` enostavno spremenili `ENGINE` na `'django.db.backends.postgresql'`. 

Kar se tiče podrobnosti konfiguracije, bi lahko uporabljali konfiguracijske datoteke, ki so specifične PostgreSQL, kot je to predlagano v dokumentaciji.
Ker pa na tej točki nočemo dodatnih komplikacij z PostgreSQL (vseeno bi raje čim več naredili v Django-tu), bomo podatke kar spisali v `default` slovar, kot je to narejeno [na primeru tu](https://docs.djangoproject.com/en/6.0/ref/settings/#std-setting-DATABASES).
Moramo torje povedati:
- HOST: IP ali domena serverja, kjer se poganja PostgreSQL
- PORT: za PostgreSQL je privzeti port 5432
- NAME: Ime konkretne podatkovne baze na PostgreSQL
- USER: Naše uporabniško ime pri katerem imamo zadostne pravice za dano bazo
- PASSWORD: Pripadajoče geslo za našega uporabnika

Teh podatkov vseeno načeloma nočemo imeti kar tako v kodi (morda bo npr. koda na več repozitorijih), zato jih bomo spravili v prperosto konfiguracijsko datoteko s pomočjo [django-environ](https://django-environ.readthedocs.io/en/latest/). Najprej torej namestimo še Python knjižnico `django-environ`. 

Naša konfiguracija bo shranjena v datoteki `.env`, ki bo v mapi `filmi_projekt` (root našega Django projekta).
Ta datoteka je tudi že v našem `.gitignore` in se ne bo pojavila na repozitoriju.
### Primer .env datoteke
```
NAME=filmi_db
USER=nas_username
PASSWORD=nase_geslo
HOST=baza.fmf.uni-lj.si
PORT=5432
```

Pogledamo [django-environ quickstart](https://django-environ.readthedocs.io/en/latest/quickstart.html), kjer imamo lepo prikazano, kako potem dostopamo do podatkov, shranjenih v naši `.env` atoteki. S tem torej potencialno zaupnih podatkov kot so gesla ne hranimo direktno v kodi.

# TODO

Stvari, ki jih bom najbrž dodal, ampak jih nismo (in ne bomo) obravnavali na vajah.
- Dodajanje brisanje filma/oseb (trenutno je link mrtev)
- Dodajanje testov za zgornje funkcionalnosti (omejitev ocen na [0, 10] in iskanje po npr. priimku)

{% endraw %}
