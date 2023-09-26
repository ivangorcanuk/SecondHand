from django import forms


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, label='Поиск')
    checkbox = forms.BooleanField(widget=forms.CheckboxInput)
    date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")
