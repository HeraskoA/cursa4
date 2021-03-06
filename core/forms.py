from django import forms

from core.models import Repo


class AddRepoForm(forms.ModelForm):
    class Meta:
        model = Repo
        fields = ('deep_link',)


class NeuralForm(forms.Form):
    year = forms.IntegerField(label='Year')
    repo_count = forms.IntegerField(label='Count', required=False)
