#
#   Model za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

import bcrypt
from orm import Entiteta, Odnos
from orm import polje, Padajoce, Vzorec, pobrisi_tabele, ustvari_bazo

# TODO: odstrani!
from orm import conn, Kazalec
from orm import dbapi

class Uporabnik(Entiteta, vir='uporabnik.csv'):
    """
    Razred za uporabnika.
    """
    id: int = polje(samodejno=True)
    uporabnisko_ime: str = polje(enolicno=True)
    admin: bool = polje(privzeto=0)
    geslo: bytes = polje(obvezno=False, shrani=False)

    IME = 'uporabnisko_ime'

    @classmethod
    def _obdelaj_podatek(cls, vrstica):
        """
        Obdelaj podatek pred uvozom.
        """
        if vrstica["geslo"]:
            vrstica["geslo"] = cls.zgostitev(vrstica["geslo"])
        else:
            vrstica["geslo"] = None
        return vrstica

    @staticmethod
    def prijavi(uporabnisko_ime, geslo):
        """
        Vrni uporabnika z navedenim uporabniškim imenom in geslom.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        try:
            uporabnik, = Uporabnik.seznam(uporabnisko_ime=uporabnisko_ime,
                                          dodatni_stolpci=['geslo'])
        except ValueError:
            return Uporabnik.NULL
        if uporabnik.geslo and bcrypt.checkpw(geslo.encode("utf-8"), uporabnik.geslo):
            del uporabnik.geslo
            return uporabnik
        else:
            return Uporabnik.NULL

    @classmethod
    def z_id(cls, idu):
        """
        Vrni uporabnika z navedenim ID-jem.
        Če takega uporabnika ni, vrni neprijavljenega uporabnika.
        """
        try:
            return super().z_id(idu)
        except ValueError:
            return cls.NULL

    @staticmethod
    def zgostitev(geslo):
        """
        Vrni zgostitev podanega gesla.
        """
        sol = bcrypt.gensalt()
        return bcrypt.hashpw(geslo.encode("utf-8"), sol)

    def dodaj(self, geslo, transakcija=True):
        """
        Dodaj uporabnika v bazo z navedenim geslom.
        """
        assert self.uporabnisko_ime, "Uporabniško ime ni določeno!"
        zgostitev = self.zgostitev(geslo)
        super().dodaj(transakcija, geslo=zgostitev)

    def spremeni_geslo(self, geslo):
        """
        Spremeni uporabnikovo geslo.
        """
        self.posodobi(geslo=self.zgostitev(geslo))


class Oznaka(Entiteta, kljuc='kratica', uredi=['kratica']):
    """
    Razred za oznako filma.
    """

    kratica: str = polje()

    IME = 'kratica'


class Film(Entiteta, vir='film.csv'):
    """
    Razred za film.
    """

    id: int = polje(samodejno=True)
    naslov: str = polje()
    dolzina: int = polje()
    leto: int = polje()
    ocena: float = polje()
    metascore: int = polje(obvezno=False)
    glasovi: int = polje(privzeto=0)
    zasluzek: int = polje(obvezno=False)
    oznaka: Oznaka = polje(obvezno=False)
    opis: str = polje(obvezno=False)

    IME = 'naslov'

    @classmethod
    def _obdelaj_podatek(cls, vrstica):
        """
        Obdelaj podatek pred uvozom.
        """
        if vrstica['oznaka']:
            try:
                Oznaka.z_id(vrstica['oznaka'])
            except ValueError:
                Oznaka(vrstica['oznaka']).dodaj(False)
        else:
            vrstica['oznaka'] = None
        return vrstica

    @staticmethod
    def najboljsi_v_letu(leto, n=10):
        """
        Vrni najboljših n filmov v danem letu.
        """
        yield from Film.seznam(leto=leto, uredi=[Padajoce('ocena')], omejitev=n)

    def zasedba(self):
        """
        Vrni seznam vseh oseb,
        ki so sodelovale pri filmu self:
        najprej režiserji, potem igralci,
        v ustreznem vrstnem redu
        """
        sql = """
            SELECT oseba.id, oseba.ime, vloga.tip, vloga.mesto
              FROM oseba
              JOIN vloga ON oseba.id = vloga.oseba
             WHERE vloga.film = ?
             ORDER BY tip DESC, mesto;
        """
        with Kazalec() as cur:
            cur.execute(sql, [self.id])
            yield from (Vloga(self, Oseba(oid, ime), tip, mesto)
                        for oid, ime, tip, mesto in cur)

class Oseba(Entiteta, vir='oseba.csv'):
    """
    Razred za osebo.
    """
    id: int = polje(samodejno=True)
    ime: str = polje()

    IME = 'ime'

    def poisci_vloge(self):
        """
        Vrni seznam vseh filmov, kjer
        je oseba self imela vlogo, 
        urejeno po letih
        """
        sql = """
            SELECT film.id, film.naslov, film.leto, vloga.tip, vloga.mesto
              FROM film
              JOIN vloga ON film.id = vloga.film
             WHERE vloga.oseba = ?
             ORDER BY leto;
        """
        with Kazalec() as cur:
            cur.execute(sql, [self.id])
            yield from (Vloga(Film(fid, naslov, leto=leto), self, tip, mesto)
                        for fid, naslov, leto, tip, mesto in cur)

    @staticmethod
    def poisci(niz):
        """
        Vrni vse osebe, ki v imenu vsebujejo dani niz.
        """
        yield from Oseba.seznam(ime=Vzorec('%' + niz + '%'))


class Zanr(Entiteta):
    """
    Razred za žanr.
    """

    id: int = polje(samodejno=True)
    naziv: str = polje(enolicno=True)

    IME = 'naziv'


class Vloga(Odnos, vir='vloga.csv', enolicnost=[('film', 'tip', 'mesto')]):
    """
    Razred za vlogo.
    """

    film: Film = polje()
    oseba: Oseba = polje()
    tip: str = polje(kljuc=True)
    mesto: int = polje()

    VLOGE = {'I': 'igralec', 'R': 'režiser'}

    def __str__(self):
        """
        Znakovna predstavitev vloge.
        """
        return f"{self.oseba}: {self.tip_vloge} {self.mesto} v filmu {self.film}"

    @property
    def tip_vloge(self):
        return self.VLOGE[self.tip]


class Pripada(Odnos, vir='zanr.csv'):
    """
    Razred za pripadnost filma žanru.
    """

    film: Film = polje()
    zanr: Zanr = polje()

    def __str__(self):
        """
        Znakovna predstavitev pripadnosti.
        """
        return f"{self.film} pripada žanru {self.zanr}"

    @classmethod
    def _obdelaj_podatek(cls, vrstica):
        """
        Obdelaj podatek pred uvozom.
        """
        try:
            zanr, = Zanr.seznam(naziv=vrstica['naziv'])
        except ValueError:
            zanr = Zanr(naziv=vrstica['naziv'])
            zanr.dodaj(False)
        vrstica['zanr'] = zanr.id
        del vrstica['naziv']
        return vrstica

