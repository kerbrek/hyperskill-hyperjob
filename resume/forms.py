from django.forms import ModelForm

from .models import Resume


class NewResumeForm(ModelForm):
    class Meta:
        model = Resume
        fields = ['description']
