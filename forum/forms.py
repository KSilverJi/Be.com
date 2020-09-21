from django import forms
from .models import Forum

class ForumUpdate(forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['title','body','writer']#writer 추가
