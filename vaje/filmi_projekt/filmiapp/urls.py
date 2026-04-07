from django.urls import path
from . import views

app_name = 'filmiapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:film_id>', views.film_podrobnosti, name='film_podrobnosti'),
    path('najboljsi/<int:st_najboljsih>', views.film_najboljsi, name='film_najboljsi'),
    path('film_poisci', views.film_poisci, name='film_poisci'),
    path('film_dodaj', views.film_dodaj, name='film_dodaj'),
    path('glasuj', views.film_glasuj, name='film_glasuj'),
]
