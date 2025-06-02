# forms.py
from django import forms
from .models import VolunteerApplication

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Your Name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message'}))




class VolunteerForm(forms.ModelForm):
    class Meta:
        model = VolunteerApplication
        fields = ['name', 'email', 'phone', 'skills', 'availability']


from django import forms
from .models import PartnershipApplication

class PartnershipApplicationForm(forms.ModelForm):
    class Meta:
        model = PartnershipApplication
        fields = ['name', 'email', 'organization', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'organization': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter organization (optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us how you’d like to partner', 'rows': 5}),
        }
