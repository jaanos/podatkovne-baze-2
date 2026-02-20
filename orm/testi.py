from model import Uporabnik, Oznaka, Film, Oseba, Zanr, Vloga, Pripada
from model import pobrisi_tabele, ustvari_bazo

pobrisi_tabele()
ustvari_bazo()

micka = Uporabnik(uporabnisko_ime='micka')
micka.dodaj('geselce')
assert micka.id == Uporabnik.prijavi('micka', 'geselce').id
assert not Uporabnik.prijavi('janez', 'geselce')

assert len(list(Oznaka.seznam())) == 11

pb2 = Film(naslov='Podatkovne baze 2', dolzina=100, leto=2026, ocena=10)
pb2.dodaj()
assert pb2.id == 10324145

pb2.opis = 'Zelo zanimiv film!'
pb2.posodobi()
assert Film.z_id(pb2.id).opis == pb2.opis

naj2008, = Film.najboljsi_v_letu(2008, 1)
assert len(list(naj2008.zasedba())) == 5

pitt, = Oseba.poisci('Brad Pitt')
assert len(list(pitt.poisci_vloge())) == 39
