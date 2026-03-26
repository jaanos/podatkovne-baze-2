from django.urls import path
from . import views

app_name = 'filmiapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('film/<int:film_id>', views.film_podrobnosti, name='film_podrobnosti'),
    path('najboljsi/<int:st_najboljsih>', views.film_najboljsi, name='film_najboljsi'),
]
