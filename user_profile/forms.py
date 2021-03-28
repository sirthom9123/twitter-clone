from django import forms

class InvitationForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={
                            'size':32, 
                            'placeholder': 'Email address of friend', 
                            'class': 'form-control search-query'
                            }))