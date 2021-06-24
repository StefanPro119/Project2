from django.forms import ModelForm
from . import models
from django import forms
from .models import Category


choices = Category.objects.all().values_list('name','name')

choice_list = []

for item in choices:
    choice_list.append(item)

class CreateAuction(forms.ModelForm):
    class Meta:
        model = models.Auction
        fields = ['title', 'subtitle','select_category', 'start_bit', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Title of the product'}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Text'}),
            'start_bit': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'For your product start bid will be...'}),
            'select_category': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
        }


class MakeBid(forms.ModelForm):
    class Meta:
        model = models.Bid
        fields = ['bid_value']


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        ordering = ['-date']
        fields = ['commments']



        #it will hide label 'commments'
        labels = {
            'commments': '',
        }

        widgets = {
            'commments': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Text', 'style': 'height: 150px;width:500px'}),
        }