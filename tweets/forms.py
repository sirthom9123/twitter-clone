from django import forms

class TweetForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea
                           (attrs={'rows': 1, 'cols': 85, 'class': 'form-control', 'placeholder': 'Post a new tweet...'}), 
                           max_length=160)
    country = forms.CharField(widget=forms.HiddenInput())
    
    
    
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', widget=forms.TextInput(attrs={'size': 32, 'class': 'form-control'}))
    
    
class SearchHashTagForm(forms.Form):
    query = forms.CharField(label='Enter keyword to search hashTag for',
                            widget=forms.TextInput(attrs={'size': 32, 'class':'form-control search-hash-tag-query typeahead'}))