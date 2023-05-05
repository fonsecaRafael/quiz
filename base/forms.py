from django.forms import ModelForm
from base.models import Player


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'email']
