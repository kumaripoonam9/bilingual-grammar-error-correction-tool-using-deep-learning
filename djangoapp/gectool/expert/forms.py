from django import forms
from .models import ExpertLanguage, Message


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
        fields = ('languages_known','cerificates')




class InputMessageForm(forms.ModelForm):
    attachment = forms.FileField(
        required = False,
        widget = forms.ClearableFileInput(
            attrs={'class':'m-auto form-control form-control-sm'})
    )
    message = forms.CharField(
        required = False,
        widget = forms.Textarea(
            attrs={'rows':'2', 
                   'class': 'form-control'})
    )

    class Meta:
        model = Message
        fields = ('message', 'attachment')

# class FileUploadForm(forms.Form):
#     file = forms.FileField(
#         required=True,
#         widget = forms.ClearableFileInput(
#             attrs={
#                 'class':'m-auto w-75 form-control form-control-lg',
#                 'accept':'.doc,.docx,.pdf,.txt'})
#     )