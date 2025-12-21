from django import forms
from .models import Contact
from captcha.fields import CaptchaField

class NameForm(forms.Form):
    name=forms.CharField(max_length=255)
    email=forms.EmailField()
    subject=forms.CharField(max_length=255)
    message=forms.CharField(widget=forms.Textarea())

class ContactForm(forms.ModelForm):
    captcha = CaptchaField()
    class Meta:
        model=Contact
        fields="__all__"
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subject'].required = False