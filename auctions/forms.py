from django.forms import ModelForm
from . import models
from django import forms
# from .models import Category


# choices = Category.objects.all().values_list('name','name')
#
# choice_list = []
#
# for item in choices:
#     choice_list.append(item)

class CreateAuction(forms.ModelForm):
    class Meta:
        model = models.Auction
        fields = ['title', 'subtitle', 'start_bit', 'image']

        widgets = {
            'title': forms.TextInput(attrs={'class':'form-control'}),
            'subtitle': forms.Textarea(attrs={'class': 'form-control'}),
            'start_bit': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'select_category': forms.Select(choices=choice_list, attrs={'class':'form-control'}),
        }