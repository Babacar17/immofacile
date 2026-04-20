from django import forms
from .models import Listing

W = lambda cls, **kw: cls(attrs={'class': 'form-control', **kw})

class ListingForm(forms.ModelForm):
    class Meta:
        model   = Listing
        exclude = ('owner','status','views_count','created_at','updated_at','is_featured','slug')
        widgets = {
            'title':         W(forms.TextInput,   placeholder='Ex: Appartement F3 meublé, Plateau'),
            'description':   W(forms.Textarea,    rows=5),
            'type':          W(forms.Select),
            'country':       W(forms.TextInput),
            'city':          W(forms.TextInput,   placeholder='Ex: Dakar'),
            'neighborhood':  W(forms.TextInput,   placeholder='Ex: Plateau, Mermoz'),
            'address':       W(forms.TextInput,   placeholder='Ex: Rue 10 x Avenue Cheikh Anta Diop'),
            'price':         W(forms.NumberInput, placeholder='Ex: 150000'),
            'price_charges': W(forms.NumberInput, placeholder='0'),
            'deposit':       W(forms.NumberInput, placeholder='0'),
            'surface':       W(forms.NumberInput, placeholder='Ex: 65'),
            'rooms':         W(forms.NumberInput, min=1, max=20),
            'bedrooms':      W(forms.NumberInput, min=0, max=20),
            'bathrooms':     W(forms.NumberInput, min=1, max=10),
            'floor':         W(forms.NumberInput, min=0),
            'latitude':      W(forms.NumberInput, step='any', placeholder='Ex: 14.6928'),
            'longitude':     W(forms.NumberInput, step='any', placeholder='Ex: -17.4467'),
            'available_from':W(forms.DateInput,   type='date'),
        }

class ListingSearchForm(forms.Form):
    q         = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Quartier, ville, description...'}))
    type      = forms.ChoiceField(required=False, choices=[('','Tous types')]+list(Listing.Type.choices), widget=forms.Select(attrs={'class':'form-control form-select'}))
    city      = forms.CharField(required=False, widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Ex: Dakar'}))
    price_max = forms.IntegerField(required=False, widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Budget max'}))
