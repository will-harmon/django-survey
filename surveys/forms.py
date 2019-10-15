from django.forms.formsets import formset_factory
from django.forms import ModelForm, inlineformset_factory

from .models import Survey, Choice


class SurveyForm(ModelForm):
    class Meta:
        model = Survey
        fields = ('survey_text',)

class ChoiceForm(ModelForm):
    class Meta:
        model = Choice
        fields = ('choice_text',)

ChoiceFormSet = formset_factory(ChoiceForm, extra=0, min_num=2, validate_min=True)
