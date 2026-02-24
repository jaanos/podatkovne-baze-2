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


def polje(kljuc=None, samodejno=None, enolicno=False, obvezno=True, privzeto=None):
    """
    Funkcija, ki vrne polje za dataclass.
    """
    return field(default=privzeto,
                 metadata=dict(
                     kljuc=kljuc,
                     samodejno=samodejno,
                     enolicno=enolicno,
                     obvezno=obvezno,
                    ))


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


class Tabela:
    """
    Nadrazred za tabele.
    """

    TABELE = []

    def __init_subclass__(cls, /, dodaj=False, enolicnost=[], **kwargs):
        """
        Inicializacija podrazreda.

        Doda podrazred v seznam tabel.
        """
        super().__init_subclass__(**kwargs)
        if dodaj:
            cls.TABELE.append(cls)
            cls.ENOLICNOST = enolicnost
            dataclass(cls)
            dataclass_json(cls)

    @classmethod
    def uvozi_podatke(cls, cur=None):
        """
        Uvozi podatke v tabelo.

        Privzeto ne naredi ničesar, podrazredi naj povozijo definicijo.
        """
        pass

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
        yield cls.KLJUC


class Odnos(Tabela):
    def __init_subclass__(cls, /, **kwargs):
        """
        Inicializacija podrazreda.
        """
        super().__init_subclass__(dodaj=True, **kwargs)

    @classmethod
    def _kljuc(cls):
        for f in fields(cls):
            if f.metadata['kljuc'] or \
                    (f.metadata['kljuc'] is None and issubclass(f.type, Entiteta)):
                yield f


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
            with conn:
                cur.execute("PRAGMA foreign_keys = OFF;")
                if pobrisi:
                    pobrisi_tabele(cur=cur)
                ustvari_tabele(cur=cur)
                uvozi_podatke(cur=cur)
        finally:
            cur.execute("PRAGMA foreign_keys = ON;")
