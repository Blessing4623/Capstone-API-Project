from django import forms
from .models import Book
class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ('title', 'author', 'publication_year')
        labels ={
            'title': 'Title',
            'author': 'author',
            'publication_year': 'publication_year'
        }
        widgets = {
            'title': forms.TextInput(),
            'author': forms.TextInput(),
            'publication_year': forms.TextInput()
        }