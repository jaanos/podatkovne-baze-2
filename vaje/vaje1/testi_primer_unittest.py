"""
Ta skripta služi kot demonstracija sintakse unittest knjižnice.
Če jo želite preizkusiti jo najprej prekopirajte v orm/ mapo (da bodo pravilno
delali importi, saj jih nismo spreminjali)
"""

import unittest
from model import Uporabnik, Oznaka, Film, Oseba, Zanr, Vloga, Pripada
from model import pobrisi_tabele, ustvari_bazo
from model import conn


def setUpModule():
    """
    Za pripravo testov se uporabljajo funkcije s točno določenim imenom npr.
    setUpModule je na nivoju modula
    (kot primer sem premaknemo kodo za ustvarjanje baze).
    """
    pobrisi_tabele()
    ustvari_bazo()
    # Izpisovanje poizvedb, zaenkrat zakomentirano, da je manj teksta.
    # conn.set_trace_callback(print)


class TestModel(unittest.TestCase):
    """
    Testi se organizirajo v classe, ime je tipično Test...
    classi dedujejo od unittest.TestCase.

    Posamezni testi (ali skupek testov) so potem metode tega
    classa (glej naprej).
    Testi, ki sledijo niso povsem neodvisni (na te stvari je treba pazit pri
    unit testih), ampak za demonstracijo bo v redu.
    """

    def test_uporabnik(self):

        micka = Uporabnik(uporabnisko_ime='micka')
        micka.dodaj('geselce')

        # Če želimo, da test uspe v prieru, da sta želeni stvari enaki,
        # uporabimo self.assertEqual.
        # Podobni "asserti" obstajajo za mnogo stvari: assertAlmostEqual,
        # assertNotEqual,... Celo assertRaise, če želimo preveriti, da se
        # napake pravilno prožijo.
        self.assertEqual(micka.id, Uporabnik.prijavi('micka', 'geselce').id)
        self.assertFalse(Uporabnik.prijavi('janez', 'geselce'))

    def test_seznam(self):
        self.assertEqual(len(list(Oznaka.seznam())), 11)

    def test_film(self):
        pb2 = Film(naslov='Podatkovne baze 2', dolzina=100, leto=2026,
                   ocena=10)
        pb2.dodaj()
        self.assertEqual(pb2.id, 10324145)
        self.assertEqual(len(list(Film.najboljsi_v_letu(2026))), 1)
        pb2.opis = 'Zelo zanimiv film!'
        pb2.posodobi()
        self.assertEqual(Film.z_id(pb2.id).opis, pb2.opis)
        pb2.izbrisi()
        self.assertEqual(len(list(Film.najboljsi_v_letu(2026))), 0)
        naj2008, = Film.najboljsi_v_letu(2008, 1)
        self.assertEqual(len(list(naj2008.zasedba())), 5)

    def test_oseba(self):
        pitt, = Oseba.poisci('Brad Pitt')
        self.assertEqual(len(list(pitt.poisci_vloge())), 39)


if __name__ == "__main__":
    # unittest.main() bo izvedel teste. Če v argument damo še verbosity=2,
    # bomo dobili natančenjši izpit vseh testov, ki so se uspešno izvedli,
    # sicer pa le tistih, ki se niso uspešno izvedli.
    unittest.main()
