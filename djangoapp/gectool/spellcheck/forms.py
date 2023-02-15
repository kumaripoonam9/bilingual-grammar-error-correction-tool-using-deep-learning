from django import forms 

class FileUploadForm(forms.Form):
    file = forms.FileField(
        required=True,
        widget = forms.ClearableFileInput(
            attrs={
                'class':'m-auto w-75 form-control form-control-lg',
                'accept':'.doc,.docx,.pdf,.txt'})
    )
        
    # for creating file input
    # attrs={'class':'m-auto w-75 form-control form-control-lg','accept':'.doc,.docx,.pdf,.txt'}