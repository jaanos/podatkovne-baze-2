from django.contrib import admin
from .models import Oseba, Oznaka, Film, Zanr, Vloga


admin.site.register(Oseba)
admin.site.register(Oznaka)
admin.site.register(Film)
admin.site.register(Zanr)
admin.site.register(Vloga)