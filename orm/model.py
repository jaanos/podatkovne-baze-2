#
#   Model za delo z bazo filmi.sqlite
#
#   J. Vidali, nov. 2024
#   Prirejeno po M. Pretnar, 2019, M. Lokar, dec. 2020
#

import bcrypt
from orm import Entiteta, Odnos
from orm import polje, pobrisi_tabele, ustvari_bazo

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
        sql = """
          SELECT id, uporabnisko_ime, admin, geslo
            FROM uporabnik WHERE uporabnisko_ime = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [uporabnisko_ime])
            vrstica = cur.fetchone()
            if vrstica is None:
                return Uporabnik.NULL
            *data, zgostitev = vrstica
            if zgostitev and bcrypt.checkpw(geslo.encode("utf-8"), zgostitev):
                return Uporabnik(*data)
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

    def dodaj(self, geslo):
        """
        Dodaj uporabnika v bazo z navedenim geslom.
        """
        assert self.uporabnisko_ime, "Uporabniško ime ni določeno!"
        zgostitev = self.zgostitev(geslo)
        super().dodaj(geslo=zgostitev)

    def spremeni_geslo(self, geslo):
        """
        Spremeni uporabnikovo geslo.
        """
        assert self.id, "Uporabnik še ni vpisan v bazo!"
        sql = """
          UPDATE uporabnik SET geslo = ?
           WHERE id = ?;
        """
        zgostitev = self.zgostitev(geslo)
        with Kazalec() as cur:
            with conn:
                cur.execute(sql, [zgostitev, self.id])


class Oznaka(Entiteta, kljuc='kratica'):
    """
    Razred za oznako filma.
    """

    kratica: str = polje()

    IME = 'kratica'

    @staticmethod
    def seznam():
        sql = """
            SELECT kratica FROM oznaka
            ORDER BY kratica;
        """
        with Kazalec() as cur:
            cur.execute(sql)
            yield from (Oznaka(kratica) for kratica, in cur)

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
                Oznaka(vrstica['oznaka']).dodaj()
        else:
            vrstica['oznaka'] = None
        return vrstica

    @staticmethod
    def najboljsi_v_letu(leto, n=10):
        """
        Vrni najboljših n filmov v danem letu.
        """
        sql = """
            SELECT id, naslov, dolzina, leto, ocena
              FROM film
             WHERE leto = ?
             ORDER BY ocena DESC
             LIMIT ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [leto, n])
            yield from (Film(*vrstica) for vrstica in cur)

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
        sql = """
            SELECT id, ime FROM oseba WHERE ime LIKE ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, ['%' + niz + '%'])
            yield from (Oseba(*vrstica) for vrstica in cur)


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
            zanr, = Zanr.poisci(naziv=vrstica['naziv'])
        except ValueError:
            zanr = Zanr(naziv=vrstica['naziv'])
            zanr.dodaj()
        vrstica['zanr'] = zanr.id
        del vrstica['naziv']
        return vrstica

