import re
from django import forms


class ObservationalWidget(forms.MultiWidget):

    def __init__(self, choices, *args, **kwargs):
        self.choices = choices
        self.widgets = []
        for _, choice in choices:
            self.widgets = self.widgets + [forms.NumberInput()]

        super(ObservationalWidget, self).__init__(self.widgets, *args, **kwargs)

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        rendered_html = self._render(self.template_name, context, renderer)

        split_html = re.findall('\<input.*?\>', rendered_html)
        processed_html = ['<label>' + self.get_choice(self.choices, input, split_html) + '</label>' + input for input in split_html]

        final_html = ''.join(processed_html)

        return final_html

    def get_choice(self, choices, input, string):
        index = string.index(input)
        _, choice = choices[index]
        return choice

    def decompress(self, value):
        if value:
            return value.split(' ')
        return [None, None]
