from django import forms
from .models import ExpertLanguage


class ExpertLanguageForm(forms.ModelForm):
    LANGUAGES = [
        ('Hindi', 'Hindi'),
        ('English', 'English'),
        ('Both hindi and english', 'Both hindi and english')]
    # languages_known = forms.CharField(
    #     choices=LANGUAGES,
    #     widget=forms.CheckboxSelectMultiple,
    # )
    languages_known = forms.ChoiceField(choices=LANGUAGES)

    class Meta:
        model = ExpertLanguage
        fields = ('languages_known',)
