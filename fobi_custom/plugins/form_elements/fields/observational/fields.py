from django import forms


class ObservationalField(forms.MultiValueField):
    def __init__(self, choices=None, *args, **kwargs):
        fields = [forms.IntegerField(label="ldkfjs")] * len(choices)
        self.choices = choices
        super(ObservationalField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        choices_cleaned = [choice[0] for choice in self.choices]
        saved_data = list(zip(choices_cleaned, data_list))

        return saved_data
