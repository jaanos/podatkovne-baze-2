# 1. Vaje

Na 1. vajah smo si pogledali nekaj pogostih orodij, ki jih lahko uporabljamo med razvijanjem Python aplikacij.
Seveda so vsa ta orodja le pripomoček in jih ne bomo nujno rabili za nadaljne delo pri predmetu.

## venv

Naučili (ponovili?) smo kako lahko v Python-u enostavno naredimo virtualno okolje [venv](https://docs.python.org/3/library/venv.html).
To storimo z ukazom (morda boste morali namesto *python* uporabiti *python3*)
`python -m venv "ime datoteke"`
Ime je pogosto kar "venv". Aktivacija okolja je odvisna od operacijskega sistema: 
Windows: `"ime_datoteteke"/Scripts/Activate`
Linux: `source "ime datoteke"\bin\activate`
Po aktivaciji se nam na začetku terminala izpiše (venv) ali (base). Virtualno okolje lahko deaktiviramo z `deactivate`.
Ko smo v virtualnem okolju, lahko inštaliramo poljubne knjižnice (z npr. `pip install`) in bodo te vidne le v virtualnem okolju.
To delamo, ker ponavadi nočemo z preveč knjižnicami "umazati" naše glavno okolje, pa tudi ker pogosto kakšni projekti potrebujejo točno določene verzije knjižnic, oziroma morda delamo na več projektih hkrati...

## pip

Ponovili smo tudi osnove Python-ovega Package Managerja in z njim namestili Django kot enostavno:
`pip install django`
Uspešnost inštalacije lahko enostavno preverimo, če odpremo python (`python`) in poskusimo importat Django (`import django`).

V nadaljevanju smo si pogledali še primer uporabe requirements.txt datoteke, kamor lahko shranimo seznam knjižnic, da nam jih ni treba vedno eno po eno nameščat (to datoteko boste pogosto videli na kakšnih repozitorijih raznih Python projektov).
Recimo, da v golem ("vanilla") Python okolju inštaliramo vse kar želimo (na vajah smo inštalirali vse dodatne knjižnice, ki jih potrebuje profesorjev orm). Inštalirane verzije si shranimo v fajl enostavno z:
`pip freeze > requirements.txt`.
Nekdo drug (kolega, sodelavec, obiskovalec našega repozitorija) si s pomočjo te datoteke lahko na hitro naloži vse potrebno z
`pip install -r requirements.txt`.

## linterji

Na vajah smo si pogledali nekaj linter orodij, ki jih lahko uporabljamo za lepšanje kode.
S **flake8** lahko preverjamo skladnost z [uradnimi Python stilskimi smernicami](https://peps.python.org/pep-0008/), opozarja pa nas tudi na druge napake (videli smo npr., da opozori na neuporabljene importe).
**pylint** je še nekoliko zahtevnejši, videli smo npr., da se pritoži tudi ob manjkajočih docstringih v kodi.
Omenjal sem še **mypy**, s pomočjo katerega lahko v Python dodamo še tipe, kot v marsikaterih drugih jezikih.
Ta orodja lahko ženemo iz terminala (inštalacija s `pip`), v praksi pa jih namestimo kar kot VSCode extension.

## unit testi

Na koncu smo omenili še testiranje - dandanes je nezanemarljiv del dolžnosti programerja tudi pisanje testov. V resnih projektih se pričakuje, da vsak programer poleg razvoja npr. nove funkcionalnosti zanjo doda še primerne teste. Pred vsakem push-om na glavni repozitorij se potem poženejo vsi (ali določen izbor) testi, da minimiziramo verjetnost za hrošče v kodi.
Pogledali smo si kako lahko teste iz predavanj napišemo s pomočjo knjižnice `unittest`.
`unittest` je priporočen tudi na Django-tovi spletni strani, vendar se dandanes pogosto uporabljajo druge knjižnice za testiranje (`pytest`).
