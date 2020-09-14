from django import forms

from .models import MarketingPreferences

class MarketingPreferencesForm(forms.ModelForm):
    subscribed = forms.BooleanField(label="Receive Marketing Email?", required=False)
    class Meta:
        model=MarketingPreferences
        fields=['subscribed']