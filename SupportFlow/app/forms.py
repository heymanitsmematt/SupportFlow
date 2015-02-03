"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _

class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class NodeEdit(forms.Form):
    #parent = forms.CharFie(Parent) create parent element in view
    node_name = forms.CharField(widget=forms.Select, max_length=100)
    node_description = forms.CharField(max_length = 200, widget=forms.Textarea)
    image_folder = forms.FileField()
    details = forms.CharField(max_length = 10000, widget=forms.Textarea)





