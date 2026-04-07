from django.forms import ModelForm, TextInput, NumberInput, Select
from .models import Film


class BulmaFormMixin:
    def __init__(self, /, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (TextInput, NumberInput)):
                field.widget.attrs.update({'class': 'input'})
            elif isinstance(field.widget, Select):
                field.widget.template_name = "forms/select_snippet.html"


class FilmForm(BulmaFormMixin, ModelForm):
    template_name = "forms/form_snippet.html"

    class Meta:
        model = Film
        exclude = ["vloge"]
