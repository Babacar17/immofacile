from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Prénom', max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Votre prénom'}))
    last_name  = forms.CharField(label='Nom',    max_length=50, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Votre nom'}))
    email      = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'vous@email.com'}))
    phone      = forms.CharField(label='Téléphone', max_length=20, required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'+221 77 000 00 00'}))

    class Meta:
        model  = User
        fields = ('username','first_name','last_name','email','phone','role','password1','password2')
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control','placeholder':'nom_utilisateur'}),
            'role':     forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class':'form-control','placeholder':'Min. 8 caractères'})
        self.fields['password2'].widget.attrs.update({'class':'form-control','placeholder':'Répétez le mot de passe'})

class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control','placeholder':'Nom d\'utilisateur'})
        self.fields['password'].widget.attrs.update({'class':'form-control','placeholder':'Mot de passe'})

class ProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ('first_name','last_name','email','phone','whatsapp','avatar','bio','city','agency_name','agency_address','agency_website','agency_license','notify_messages','notify_visits')
        widgets = {
            'first_name':     forms.TextInput(attrs={'class':'form-control'}),
            'last_name':      forms.TextInput(attrs={'class':'form-control'}),
            'email':          forms.EmailInput(attrs={'class':'form-control'}),
            'phone':          forms.TextInput(attrs={'class':'form-control','placeholder':'+221 77 000 00 00'}),
            'whatsapp':       forms.TextInput(attrs={'class':'form-control','placeholder':'+221 77 000 00 00'}),
            'bio':            forms.Textarea(attrs={'class':'form-control','rows':3}),
            'city':           forms.TextInput(attrs={'class':'form-control','placeholder':'Dakar'}),
            'agency_name':    forms.TextInput(attrs={'class':'form-control'}),
            'agency_address': forms.TextInput(attrs={'class':'form-control'}),
            'agency_website': forms.URLInput(attrs={'class':'form-control'}),
            'agency_license': forms.TextInput(attrs={'class':'form-control'}),
        }
