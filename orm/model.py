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

class Uporabnik(Entiteta):
    """
    Razred za uporabnika.
    """
    id: int = polje()
    uporabnisko_ime: str = polje(enolicno=True)
    admin: bool = polje(privzeto=0)
    geslo: bytes = polje(obvezno=False)

    IME = 'uporabnisko_ime'
    VIR = 'uporabnik.csv'

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "uporabnik".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS uporabnik;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "uporabnik".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                if vrstica["geslo"]:
                    vrstica["geslo"] = cls.zgostitev(vrstica["geslo"])
                else:
                    vrstica["geslo"] = None
                cur.execute("""
                    INSERT INTO uporabnik (uporabnisko_ime, admin, geslo)
                    VALUES (:uporabnisko_ime, :admin, :geslo);
                """, vrstica)

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
        sql = """
          SELECT id, uporabnisko_ime, admin
            FROM uporabnik WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [idu])
            vrstica = cur.fetchone()
            if vrstica is None:
                return cls.NULL
            return cls(*vrstica)

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
        assert not self.id, "Uporabnik je že vpisan v bazo!"
        assert self.uporabnisko_ime, "Uporabniško ime ni določeno!"
        sql = """
          INSERT INTO uporabnik (uporabnisko_ime, geslo, admin)
          VALUES (?, ?, ?);
        """
        zgostitev = self.zgostitev(geslo)
        with Kazalec() as cur:
            try:
                with conn:
                    cur.execute(sql, [self.uporabnisko_ime, zgostitev, self.admin])
                self.id = cur.lastrowid
            except dbapi.IntegrityError:
                raise ValueError("Uporabniško ime že obstaja!")

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

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "oznaka".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS oznaka;
            """)

    @staticmethod
    def seznam():
        sql = """
            SELECT kratica FROM oznaka
            ORDER BY kratica;
        """
        with Kazalec() as cur:
            cur.execute(sql)
            yield from (Oznaka(kratica) for kratica, in cur)

class Film(Entiteta):
    """
    Razred za film.
    """

    id: int = polje()
    naslov: str = polje()
    dolzina: int = polje()
    leto: int = polje()
    ocena: float = polje()
    metascore: int = polje(obvezno=False)
    glasovi: int = polje(privzeto=0)
    zasluzek: int = polje(obvezno=False)
    oznaka: Oznaka = polje(obvezno=False)
    opis: str = polje(obvezno=False)

    VIR = "film.csv"
    IME = 'naslov'

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "film".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS film;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabeli "film" in "oznaka".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                if vrstica['oznaka']:
                    cur.execute("""
                        SELECT kratica FROM oznaka
                        WHERE kratica = :oznaka;
                    """, vrstica)
                    if not cur.fetchone():
                        cur.execute("""
                            INSERT INTO oznaka (kratica) VALUES (:oznaka);
                        """, vrstica)
                else:
                    vrstica['oznaka'] = None
                cur.execute("""
                    INSERT INTO film (id, naslov, dolzina, leto, ocena,
                                    metascore, glasovi, zasluzek, oznaka, opis)
                    VALUES (:id, :naslov, :dolzina, :leto, :ocena,
                            :metascore, :glasovi, :zasluzek, :oznaka, :opis);
                """, vrstica)

    @classmethod
    def z_id(cls, idf):
        """
        Vrni film z navedenim ID-jem.
        Če takega filma ni, sproži napako.
        """
        sql = """
          SELECT id, naslov, dolzina, leto, ocena,
                 metascore, glasovi, zasluzek, oznaka, opis
            FROM film WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [idf])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Film z ID-jem {idf} ne obstaja!")
            return Film(*vrstica)

    def dodaj(self):
        """
        Dodaj film v bazo.
        """
        assert self.id is None, "Film je že v bazi!"
        sql = """
            INSERT INTO film (naslov, dolzina, leto, ocena,
                metascore, glasovi, zasluzek, oznaka, opis)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.naslov, self.dolzina, self.leto,
                                    self.ocena, self.metascore, self.glasovi,
                                    self.zasluzek, self.oznaka, self.opis])
                    self.id = cur.lastrowid
        except dbapi.IntegrityError:
            raise ValueError("Dodajanje filma ni bilo uspešno!")

    def posodobi(self):
        """
        Posodobi film v bazi.
        """
        assert self.id is not None, "Filma še ni v bazi!"
        sql = """
            UPDATE film SET naslov = ?, dolzina = ?, leto = ?,
                ocena = ?, metascore = ?, glasovi = ?,
                zasluzek = ?, oznaka = ?, opis = ?
            WHERE id = ?;
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.naslov, self.dolzina, self.leto,
                                    self.ocena, self.metascore, self.glasovi,
                                    self.zasluzek, self.oznaka, self.opis, self.id])
        except dbapi.IntegrityError:
            raise ValueError("Posodabljanje filma ni bilo uspešno!")

    def izbrisi(self):
        """
        Izbriši film v bazi.
        """
        assert self.id is not None, "Filma še ni v bazi!"
        sql = """
            DELETE FROM film
            WHERE id = ?;
        """
        try:
            with Kazalec() as cur:
                with conn:
                    cur.execute(sql, [self.id])
                    self.id = None
        except dbapi.IntegrityError:
            raise ValueError("Brisanje filma ni bilo uspešno!")

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

class Oseba(Entiteta):
    """
    Razred za osebo.
    """
    id: int = polje()
    ime: str = polje()

    VIR = "oseba.csv"
    IME = 'ime'

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "oseba".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS oseba;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "oseba".
        """
        with Kazalec(cur) as cur:
            cur.executemany("""
                INSERT INTO oseba (id, ime)
                VALUES (:id, :ime);
            """, cls.preberi_vir())

    @classmethod
    def z_id(cls, ido):
        """
        Vrni oseob z navedenim ID-jem.
        Če take osebe ni, sproži napako.
        """
        sql = """
          SELECT id, ime
            FROM oseba WHERE id = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [ido])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Oseba z ID-jem {ido} ne obstaja!")
            return Oseba(*vrstica)

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

    id: int = polje()
    naziv: str = polje(enolicno=True)

    IME = 'naziv'

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "zanr".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS zanr;
            """)


class Vloga(Odnos, enolicnost=[('film', 'tip', 'mesto')]):
    """
    Razred za vlogo.
    """

    film: Film = polje()
    oseba: Oseba = polje()
    tip: str = polje(kljuc=True)
    mesto: int = polje()

    VIR = "vloga.csv"
    VLOGE = {'I': 'igralec', 'R': 'režiser'}

    def __str__(self):
        """
        Znakovna predstavitev vloge.
        """
        return f"{self.oseba}: {self.tip_vloge} {self.mesto} v filmu {self.film}"

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "vloga".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS vloga;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo "vloga".
        """
        with Kazalec(cur) as cur:
            cur.executemany("""
                INSERT INTO vloga (film, oseba, tip, mesto)
                VALUES (:film, :oseba, :tip, :mesto);
            """, cls.preberi_vir())

    @property
    def tip_vloge(self):
        return self.VLOGE[self.tip]


class Pripada(Odnos):
    """
    Razred za pripadnost filma žanru.
    """

    film: Film = polje()
    zanr: Zanr = polje()

    VIR = "zanr.csv"

    def __str__(self):
        """
        Znakovna predstavitev pripadnosti.
        """
        return f"{self.film} pripada žanru {self.zanr}"

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo "pripada".
        """
        with Kazalec(cur) as cur:
            cur.execute("""
                DROP TABLE IF EXISTS pripada;
            """)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabeli "pripada" in "zanr".
        """
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                cur.execute("""
                    SELECT id FROM zanr
                    WHERE naziv = :naziv;
                """, vrstica)
                rezultat = cur.fetchone()
                if rezultat:
                    vrstica["zanr"], = rezultat
                else:
                    cur.execute("""
                        INSERT INTO zanr (naziv) VALUES (:naziv);
                    """, vrstica)
                    vrstica["zanr"] = cur.lastrowid
                cur.execute("""
                    INSERT INTO pripada (film, zanr)
                    VALUES (:film, :zanr);
                """, vrstica)
