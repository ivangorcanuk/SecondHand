from django import forms
from .db_interaction_handler import DBInteractionHandler

list_sales = [
    ('Все скидки', 'Все скидки'),
    ('-30%', '-30%'),
    ('-40%', '-40%'),
    ('-60%', '-60%'),
    ('-80%', '-80%')
             ]

list_discounts = [('Все акции', 'Все акции')]
db = DBInteractionHandler()
base_sale = db.base_non_repeat_sale
for discount in base_sale:
    if discount is not None:
        list_discounts.append((discount, discount))


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': "search",
                                                                           'class': "form-control",
                                                                           'placeholder': 'Поиск...'}))


class FiltersForm(forms.Form):
    checkbox_network_moda_max = forms.BooleanField(required=False, label="Мода Макс", widget=forms.CheckboxInput())
    checkbox_network_economy_city = forms.BooleanField(required=False, label="Эконом Сити", widget=forms.CheckboxInput())
    checkbox_network_adzenne = forms.BooleanField(required=False, label="Адзенне", widget=forms.CheckboxInput())
    checkbox_network_megahand = forms.BooleanField(required=False, label="Мегахенд", widget=forms.CheckboxInput())
    checkbox_size_S = forms.BooleanField(required=False, label="S", widget=forms.CheckboxInput())
    checkbox_size_M = forms.BooleanField(required=False, label="M", widget=forms.CheckboxInput())
    checkbox_size_L = forms.BooleanField(required=False, label="L", widget=forms.CheckboxInput())
    combobox_sales = forms.CharField(required=False, widget=forms.Select(choices=list_sales))
    combobox_discounts = forms.CharField(required=False, widget=forms.Select(choices=list_discounts))
    date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': "date"}))
    checkbox = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'id': "siz1"}))

