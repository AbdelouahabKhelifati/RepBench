from django import forms
from django.forms import NumberInput

ANOMALY_CHOICES = [
    ("shift", "Shift"),
    ("outlier", "Outlier"),
    ("distortion", "Distortion"),
]


class InjectionForm(forms.Form):
    ratio = forms.FloatField(label='Ratio', min_value=0, max_value=1, initial=0.1, widget=NumberInput(
        attrs={'id': "ratio_id", 'min': 1, 'max': 0, 'step': '0.05'}))
    factor = forms.FloatField(min_value=0, initial=3)
    anomaly = forms.CharField(label='Anomaly Type', widget=forms.Select(choices=ANOMALY_CHOICES, attrs={
        "class": 'multi-anomaly'}))

    def __init__(self, data_columns, ts_name="bafu", *args, **kwargs):
        super(InjectionForm, self).__init__(*args, **kwargs)
        self.fields["data_columns"] = forms.MultipleChoiceField(
            label="Inject Anomalies For:",
            widget=forms.CheckboxSelectMultiple(),
            choices=[(i, i) for i in data_columns])

        self.fields["data_set"] = forms.CharField(widget=forms.HiddenInput(), required=False, initial=ts_name)
        self.fields["seed"] = forms.IntegerField(label='seed', required=False, widget=forms.NumberInput(
            attrs={'title': 'Enter numbers Only '}))