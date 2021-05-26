from django.forms import ModelForm

from .models import Vacancy


class NewVacancyForm(ModelForm):
    class Meta:
        model = Vacancy
        fields = ['description']
