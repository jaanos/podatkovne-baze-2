from django.db import models

class Oznaka(models.Model):
    kratica = models.CharField(max_length=10)

    def __str__(self):
        return self.kratica
    
class Oseba(models.Model):
    ime = models.CharField(max_length=100)

    def __str__(self):
        return self.ime
