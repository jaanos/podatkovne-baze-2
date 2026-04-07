from django.forms import ModelForm, TextInput, NumberInput, Select, Textarea
from .models import Film


class BulmaFormMixin:
    template_name = "forms/form_snippet.html"

    def __init__(self, /, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (TextInput, NumberInput)):
                field.widget.attrs.update({'class': 'input'})
            elif isinstance(field.widget, Textarea):
                field.widget.attrs.update({'class': 'textarea'})
            elif isinstance(field.widget, Select):
                field.widget.template_name = "forms/select_snippet.html"


class FilmForm(BulmaFormMixin, ModelForm):
    class Meta:
        model = Film
        exclude = ["vloge"]
        widgets = {
            "opis": Textarea()
        }
