from django.forms import ModelForm
from . import models
from django import forms


class CreateAuction(forms.ModelForm):
    class Meta:
        model = models.Auction
        fields = ['title', 'subtitle', 'image']