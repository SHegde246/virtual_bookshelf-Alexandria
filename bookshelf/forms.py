from django import forms

from .models import Preference

class PrefForm(forms.ModelForm):

    class Meta:
        model = Preference
        fields = ('genre', 'author')
        exclude = ('user',)
        
