from django import forms
from .models import Message, VisitRequest

class MessageForm(forms.ModelForm):
    class Meta:
        model   = Message
        fields  = ('body',)
        widgets = {'body': forms.Textarea(attrs={'class':'form-control','rows':4,'placeholder':'Écrivez votre message ici...'})}

class VisitRequestForm(forms.ModelForm):
    class Meta:
        model   = VisitRequest
        fields  = ('date','time_slot','note')
        widgets = {
            'date':      forms.DateInput(attrs={'class':'form-control','type':'date'}),
            'time_slot': forms.TimeInput(attrs={'class':'form-control','type':'time'}),
            'note':      forms.Textarea(attrs={'class':'form-control','rows':3,'placeholder':'Informations supplémentaires...'}),
        }
