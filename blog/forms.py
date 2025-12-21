from django import forms
from .models import Comments,NewsletterSubscriber
from captcha.fields import CaptchaField


class ConmmentForm(forms.ModelForm):
    captcha=CaptchaField()
    class Meta:
        model=Comments
        fields=['post','name','subject','email','message']

#------------------------------------------------------------------------

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email',
            })
        }
        labels = {
            'email': '',
        }