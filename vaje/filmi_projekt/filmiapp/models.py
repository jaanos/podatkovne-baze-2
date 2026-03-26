from django.db import models

class Oznaka(models.Model):
    kratica = models.CharField(max_length=10, primary_key=True, help_text="Kratica za oznako filma, npr. PG")

    def __str__(self):
        return self.kratica

    class Meta:
        ordering = ["kratica"]
        verbose_name_plural = "Oznake"
    
class Oseba(models.Model):
    ime = models.CharField(max_length=100, verbose_name="Ime in priimek")

    def __str__(self):
        return self.ime

    class Meta:
        verbose_name_plural = "Osebe"

class Zanr(models.Model):
    naziv = models.CharField(max_length=50, unique=True, verbose_name="Naziv žanra")

    def __str__(self):
        return self.naziv

    class Meta:
        verbose_name_plural = "Žanri"

class Film(models.Model):
    naslov = models.CharField(max_length=200, verbose_name="Naslov filma")
    dolzina = models.PositiveIntegerField(verbose_name="Dolžina filma v minutah")
    leto = models.PositiveSmallIntegerField(verbose_name="Leto izida filma")
    ocena = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Ocena filma") # Omejimo to na [0,10]?
    metascore = models.PositiveSmallIntegerField(null=True, blank=True)
    glasovi = models.IntegerField(default=0, verbose_name="Število glasov za film")
    zasluzek = models.BigIntegerField(blank=True, null=True, verbose_name="Zaslužek filma (USD)")
    oznaka = models.ForeignKey(Oznaka, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Oznaka filma")
    # Opis - pazi glede null vrednosti za charfield
    opis = models.CharField(max_length=1000, blank=True, null=True, verbose_name="Opis filma", help_text="Opis filma, do 1000 znakov")
    zanri = models.ManyToManyField(Zanr, verbose_name="Žanri filma")
    vloge = models.ManyToManyField(Oseba, through="Vloga")

    def __str__(self):
        return f'{self.naslov}, {self.leto}'
    
    class Meta:
        verbose_name_plural = "Filmi"

class Vloga(models.Model):

    TIPI_VLOG = {
        "I" : "Igralec",
        "R" : "Režiser"
    }

    film = models.ForeignKey(Film, on_delete=models.CASCADE)
    oseba = models.ForeignKey(Oseba, on_delete=models.CASCADE)
    mesto = models.PositiveIntegerField()
    tip = models.CharField(max_length=20, choices=TIPI_VLOG.items())

    def __str__(self):
        return f'{self.mesto}. {self.TIPI_VLOG[self.tip].lower()} v filmu {self.film}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["film", "mesto", "tip"],
                name="enoličnost_sodelujočega_v_filmu"
            )
        ]
        verbose_name_plural = "Vloge"
