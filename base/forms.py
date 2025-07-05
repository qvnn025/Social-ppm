from django.forms import ModelForm
from .models import Room, Share
from django import forms
from usermanager.models import Profile

class PostForm(ModelForm):
    class Meta:
        model = Room
        fields = ['topic', 'name', 'description', 'image']

class PfpForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['pfp']


class ShareForm(forms.ModelForm):
    class Meta:
        model = Share
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={'rows':2, 'placeholder':'Add a comment'}),
        }