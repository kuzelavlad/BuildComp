from django import forms
from application.models import *


class ApplicationForm(forms.ModelForm):
    document = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'multiple': True}),
        label='Прикрепленные файлы',
        required=False
    )

    class Meta:
        model = Application
        fields = '__all__'
