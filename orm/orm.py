import sqlite3 as dbapi
import csv
from dataclasses import dataclass, field, fields
from dataclasses_json import dataclass_json


conn = dbapi.connect('filmi.sqlite')
conn.execute("PRAGMA foreign_keys = ON;")


TIPI = {
    int: 'INTEGER',
    str: 'TEXT',
    bool: 'INTEGER',
    float: 'REAL',
    bytes: 'BLOB'
}


def polje(kljuc=None, samodejno=None, enolicno=False, obvezno=True, shrani=True, privzeto=None):
    """
    Funkcija, ki vrne polje za dataclass.
    """
    return field(default=privzeto,
                 metadata=dict(
                     kljuc=kljuc,
                     samodejno=samodejno,
                     enolicno=enolicno,
                     obvezno=obvezno,
                     shrani=shrani,
                    ))


@dataclass
class Padajoce:
    """
    Razred za padajoče urejanje.
    """
    stolpec: str

    def __str__(self):
        """
        Vrni znakovno predstavitev padajoče ureditve.
        """
        return f"{self.stolpec} DESC"


@dataclass
class Vzorec:
    """
    Razred za vzorce za uporabo z LIKE.
    """
    vzorec: str

    def __str__(self):
        """
        Vrni znakovno  predstavitev vzorca.
        """
        return self.vzorec


class Kazalec:
    """
    Upravitelj konteksta za kazalce.
    """

    def __init__(self, cur=None):
        """
        Konstruktor upravitelja konteksta.

        Če kazalec ni podan, odpre novega, sicer uporabi podanega.
        """
        if cur is None:
            self.cur = conn.cursor()
            self.close = True
        else:
            self.cur = cur
            self.close = False

    def __enter__(self):
        """
        Vstop v kontekst z `with`.

        Vrne kazalec - ta se shrani v spremenljivko, podano z `as`.
        """
        return self.cur

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Izstop iz konteksta.

        Če je bil ustvarjen nov kazalec, se ta zapre.
        """
        if self.close:
            self.cur.close()


class Transakcija:
    """
    Upravitelj konteksta za transakcije.
    """

    def __init__(self, transakcija=True):
        """
        Konstruktor upravitelja konteksta.

        Zabeleži, ali naj se po koncu izvajanja zaključi transakcija.
        """
        self.transakcija = transakcija

    def __enter__(self):
        """
        Vstop v kontekst z `with`.
        """
        if self.transakcija:
            return conn.__enter__()

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Izstop iz konteksta.
        """
        if self.transakcija:
            conn.__exit__(exc_type, exc_value, traceback)


class Tabela:
    """
    Nadrazred za tabele.
    """

    TABELE = []

    def __init_subclass__(cls, /, dodaj=False, uredi=[],
                          vir=None, enolicnost=[], **kwargs):
        """
        Inicializacija podrazreda.

        Doda podrazred v seznam tabel.
        """
        super().__init_subclass__(**kwargs)
        if dodaj:
            cls.TABELE.append(cls)
            cls.VIR = vir
            cls.ENOLICNOST = enolicnost
            cls.UREDI = uredi
            dataclass(cls)
            dataclass_json(cls)

    @classmethod
    def preberi_vir(cls):
        """
        Preberi vir v obliki CSV in vračaj slovarje za vsako vrstico.
        """
        with open(f"podatki/{cls.VIR}", encoding='utf-8') as f:
            rd = csv.reader(f)
            stolpci = next(rd)
            for vrstica in rd:
                yield dict(zip(stolpci, vrstica))

    @classmethod
    def _ime_tabele(cls):
        """
        Vrni ime tabele.
        """
        return cls.__name__.lower()

    @staticmethod
    def _tip(f):
        """
        Vrni tip podanega polja.
        """
        if issubclass(f.type, Entiteta):
            return f.type._tip(f.type.KLJUC)
        else:
            return TIPI[f.type]

    @classmethod
    def ustvari_tabelo(cls, cur=None):
        """
        Ustvari tabelo.
        """
        stolpci = ', '.join(f"""
                {f.name} {cls._tip(f)}
                {'UNIQUE' if f.metadata['enolicno'] else ''}
                {'NOT NULL' if f.metadata['obvezno'] else ''}
                {f'DEFAULT ({f.default})' if f.default is not None else ''}
                {f'''
                    REFERENCES {f.type._ime_tabele()}
                    ({', '.join(k.name for k in f.type._kljuc())})
                  ''' if issubclass(f.type, Entiteta) else ''}
            """ for f in fields(cls))
        kljuc = ', '.join(f.name for f in cls._kljuc())
        #privzeto = [f.default for f in fields(cls) if f.default is not None]
        #print(privzeto)
        enolicnost = ', '.join((f'PRIMARY KEY ({kljuc})', *(
            f'UNIQUE ({', '.join(u)})' for u in cls.ENOLICNOST
        )))
        sql = f"""
                CREATE TABLE {cls._ime_tabele()} (
                    {stolpci},
                    {enolicnost}
                );
            """
        with Kazalec(cur) as cur:
            cur.execute(sql) #, privzeto)

    @classmethod
    def pobrisi_tabelo(cls, cur=None):
        """
        Pobriši tabelo.
        """
        with Kazalec(cur) as cur:
            cur.execute(f"""
                DROP TABLE IF EXISTS {cls._ime_tabele()};
            """)

    def dodaj(self, transakcija=True, /, **kwargs):
        """
        Dodaj objekt v bazo.
        """
        assert self._v_bazi(False), "Objekt je že v bazi"
        stolpci = [*(f.name for f in fields(self)
                     if not f.metadata['samodejno'] and f.metadata['shrani']),
                   *kwargs]
        sql = f"""
            INSERT INTO {self._ime_tabele()} ({', '.join(stolpci)})
            VALUES ({', '.join(f':{stolpec}' for stolpec in stolpci)});
        """
        try:
            with Kazalec() as cur:
                with Transakcija(transakcija):
                    cur.execute(sql,
                                {**{stolpec: getattr(self, stolpec)
                                    for stolpec in stolpci},
                                 **kwargs})
                    self._nastavi_kljuc(cur.lastrowid)
        except dbapi.IntegrityError:
            raise ValueError("Dodajanje objekta ni bilo uspešno!")

    def posodobi(self, transakcija=True, /, **kwargs):
        """
        Posodobi objekt v bazi.
        """
        assert self._v_bazi(True), "Objekta še ni v bazi"
        stolpci = [*(f.name for f in fields(self) if f.metadata['shrani']),
                   *kwargs]
        sql = f"""
            UPDATE {self._ime_tabele()}
            SET {', '.join(f'{stolpec} = :{stolpec}' for stolpec in stolpci)}
            WHERE {' AND '.join(f'{f.name} = :{f.name}' for f in self._kljuc())};
        """
        try:
            with Kazalec() as cur:
                with Transakcija(transakcija):
                    cur.execute(sql, {**{stolpec: getattr(self, stolpec)
                                         for stolpec in stolpci},
                                      **kwargs})
        except dbapi.IntegrityError:
            raise ValueError("Posodabljanje objekta ni bilo uspešno!")

    def izbrisi(self, transakcija=True):
        """
        Izbriši objekt iz baze.
        """
        assert self._v_bazi(True), "Objekta še ni v bazi"
        sql = f"""
            DELETE FROM {self._ime_tabele()}
            WHERE {' AND '.join(f'{f.name} = :{f.name}' for f in self._kljuc())};
        """
        try:
            with Kazalec() as cur:
                with Transakcija(transakcija):
                    cur.execute(sql, {f.name: getattr(self, f.name) for f in self._kljuc()})
                    self._nastavi_kljuc(None)
        except dbapi.IntegrityError:
            raise ValueError("Brisanje objekta ni bilo uspešno!")

    @classmethod
    def _obdelaj_podatek(cls, vrstica):
        """
        Obdelaj podatek pred uvozom.
        """
        return vrstica

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo.
        """
        if not cls.VIR:
            return
        with Kazalec(cur) as cur:
            for vrstica in cls.preberi_vir():
                vrstica = cls._obdelaj_podatek(vrstica)
                cur.execute(f"""
                    INSERT INTO {cls._ime_tabele()} ({', '.join(vrstica)})
                    VALUES ({', '.join(f':{stolpec}' for stolpec in vrstica)});
                """, vrstica)

    @classmethod
    def _polja(cls, dodatni_stolpci=()):
        polja = {"_": [f for f in fields(cls)
                       if f.metadata['shrani'] or f.name in dodatni_stolpci]}
        pridruzitve = []
        for f in polja["_"]:
            if issubclass(f.type, Entiteta):
                slovar, join = f.type._polja()
                polja.update({f"{f.name}_{tabela}": p for tabela, p in slovar.items()})
                pridruzitve.append((f.type._ime_tabele(), f"{f.name}__",
                                    f"_.{f.name}", f"{f.name}__.{f.type.KLJUC.name}"))
                pridruzitve.extend([
                    (ime_tabele, f"{f.name}_{tabela}", f"{f.name}_{stolpec1}",
                     f"{f.name}_{stolpec2}")
                    for ime_tabele, tabela, stolpec1, stolpec2 in join
                ])
        return (polja, pridruzitve)

    @classmethod
    def seznam(cls, /, dodatni_stolpci=(), uredi=None, omejitev=None, **kwargs):
        """
        Vrni objekt z navedenim ključem.
        Če takega objekta ni, sproži napako.
        """
        polja, join = cls._polja(dodatni_stolpci)
        stolpci = [f"{tabela}.{f.name}" for tabela, p in polja.items() for f in p]
        if kwargs:
            where = f"WHERE {' AND '.join(
                f'_.{stolpec} LIKE :{stolpec}' if isinstance(kwargs[stolpec], Vzorec)
                else f'_.{stolpec} = :{stolpec}' for stolpec in kwargs)}"
        else:
            where = ""
        if uredi is None:
            uredi = cls.UREDI
        if uredi:
            orderby = f"ORDER BY {', '.join(f"_.{stolpec}" for stolpec in uredi)}"
        else:
            orderby = ""
        if omejitev:
            limit = "LIMIT :_omejitev"
            kwargs['_omejitev'] = omejitev
        else:
            limit = ""
        sql = f"""
          SELECT {', '.join(stolpci)}
            FROM {cls._ime_tabele()} AS _
           {'\n'.join(f"LEFT JOIN {ime_tabele} AS {tabela} ON {stolpec1} = {stolpec2}"
                      for ime_tabele, tabela, stolpec1, stolpec2 in join)}
           {where}
           {orderby}
           {limit};
        """
        with Kazalec() as cur:
            cur.execute(sql, {stolpec: str(vrednost) if isinstance(vrednost, Vzorec)
                              else vrednost for stolpec, vrednost in kwargs.items()})
            yield from (cls(**dict(zip((f.name for f in polja["_"]), vrstica)))
                        for vrstica in cur)


class Entiteta(Tabela):
    """
    Nadrazred za posamezne entitetne tipe.
    """
    def __bool__(self):
        """
        Pretvorba v logično vrednost.
        """
        return getattr(self, self.IME) is not None

    def __str__(self):
        """
        Znakovna predstavitev.
        """
        return getattr(self, self.IME) if self \
            else f"<entiteta tipa {self.__class__}>"

    def __init_subclass__(cls, /, kljuc='id', **kwargs):
        """
        Inicializacija podrazreda.

        Pripravi prazen objekt.
        """
        super().__init_subclass__(dodaj=True, **kwargs)
        for f in fields(cls):
            if f.name == kljuc:
                cls.KLJUC = f
        cls.NULL = cls()

    @classmethod
    def _kljuc(cls):
        """
        Vračaj stolpce, ki sestavljajo ključ.

        Pri entitetah ključ sestoji iz enega stolpca.
        """
        yield cls.KLJUC

    def _v_bazi(self, v_bazi):
        """
        Vrni, ali je objekt (potencialno) že v bazi.

        Če ključ ni samodejno generiran, vedno vrne True.
        """
        return not self.KLJUC.metadata['samodejno'] or \
            (getattr(self, self.KLJUC.name) is not None) == v_bazi

    def _nastavi_kljuc(self, vrednost):
        """
        Nastavi samodejno generirani ključ na podano vrednost.
        """
        if self.KLJUC.metadata['samodejno']:
            setattr(self, self.KLJUC.name, vrednost)

    @classmethod
    def z_id(cls, kljuc):
        """
        Vrni objekt z navedenim ključem.
        Če takega objekta ni, sproži napako.
        """
        stolpci = [f.name for f in fields(cls) if f.metadata['shrani']]
        sql = f"""
          SELECT {', '.join(stolpci)}
            FROM {cls._ime_tabele()} WHERE {cls.KLJUC.name} = ?;
        """
        with Kazalec() as cur:
            cur.execute(sql, [kljuc])
            vrstica = cur.fetchone()
            if vrstica is None:
                raise ValueError(f"Objekt s ključem {kljuc} ne obstaja!")
            return cls(**dict(zip(stolpci, vrstica)))


class Odnos(Tabela):
    def __init_subclass__(cls, /, **kwargs):
        """
        Inicializacija podrazreda.
        """
        super().__init_subclass__(dodaj=True, **kwargs)

    @classmethod
    def _kljuc(cls):
        """
        Vračaj stolpce, ki sestavljajo ključ.
        """
        for f in fields(cls):
            if f.metadata['kljuc'] or \
                    (f.metadata['kljuc'] is None and issubclass(f.type, Entiteta)):
                yield f

    def _v_bazi(self, v_bazi):
        """
        Vrni, ali je objekt (potencialno) že v bazi.

        Vedno vrne True.
        """
        return True

    def _nastavi_kljuc(self, cur):
        """
        Nastavi samodejno generirano vrednost ključa.

        Ključ ni samodejno generiran, tako da se ne zgodi nič.
        """
        pass

def ustvari_tabele(cur=None):
    """
    Ustvari vse tabele.
    """
    with Kazalec(cur) as cur:
        for t in Tabela.TABELE:
            t.ustvari_tabelo(cur=cur)


def pobrisi_tabele(cur=None):
    """
    Pobriši vse tabele.
    """
    with Kazalec(cur) as cur:
        for t in reversed(Tabela.TABELE):
            t.pobrisi_tabelo(cur=cur)


def uvozi_podatke(cur=None):
    """
    Uvozi vse podatke.
    """
    with Kazalec(cur) as cur:
        for t in Tabela.TABELE:
            t.uvozi_podatke(cur=cur)


def ustvari_bazo(pobrisi=False, cur=None):
    """
    Ustvari tabele in uvozi podatke.
    """
    with Kazalec(cur) as cur:
        try:
            with Transakcija():
                cur.execute("PRAGMA foreign_keys = OFF;")
                if pobrisi:
                    pobrisi_tabele(cur=cur)
                ustvari_tabele(cur=cur)
                uvozi_podatke(cur=cur)
        finally:
            cur.execute("PRAGMA foreign_keys = ON;")
