# automl_settings = {
#     "time_budget": time_budget,  # in seconds
#     "metric": "accuracy",  # choice from  accuracy , micro_f1, macro_f1
#     "task": 'classification',
#     "log_file_name": "recommendation/logs/flaml.log",
#     "estimator_list": ['lgbm', 'rf', 'xgboost', 'extra_tree', 'lrl1']
# }

from django import forms

ESTIMATOR_CHOICES = [
    ('lgbm', 'LGBM'),
    ('rf', 'Random Forest'),
    ('xgboost', 'XGBoost'),
    ('extra_tree', 'Extra Tree'),
    ('lrl1', 'LRL1')
]
METRIC_CHOICES = [('accuracy', 'accuracy'), ('micro_f1', 'micro_f1'), ('macro_f1', 'macro_f1')]
TASK_CHOICES = [('classification', 'classification')]  # add more if needed


class AutomlSettingsForm(forms.Form):
    time_budget = forms.IntegerField(label='Time Budget (seconds)', initial=60, widget=forms.NumberInput(
        attrs={'id': "time_budget_id", 'min': 0, "class": 'form-control'}))
    metric = forms.CharField(label='Metric', initial='accuracy', widget=forms.Select(choices=METRIC_CHOICES, attrs={
        "class": 'form-control'}))
    # task = forms.CharField(initial='classification', widget=forms.HiddenInput(), required=False)
    estimator_list = forms.MultipleChoiceField(label='Estimators',
                                               initial=[choice[1] for choice in ESTIMATOR_CHOICES],
                                               widget=forms.CheckboxSelectMultiple(
                                                   attrs={'class': '', "name": 'estimator_list[]'}),
                                               choices=ESTIMATOR_CHOICES
                                               )

    def __init__(self, *args, **kwargs):
        super(AutomlSettingsForm, self).__init__(*args, **kwargs)
        self.fields['estimator_list'].initial = [choice[0] for choice in ESTIMATOR_CHOICES]