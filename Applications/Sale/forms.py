from django import forms


class SalesSearchForm(forms.Form):
    CHART_CHOICES = (
        ('#1', 'Bar chart'),
        ('#2', 'Pie chart'),
        ('#3', 'Line chart'),
    )

    date_from = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateTimeField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
