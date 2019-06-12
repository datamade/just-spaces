def choices_to_help_text(choices, skip_first=False):
    help_text = ''

    if skip_first:
        choices = choices[1:]

    for _, choice in choices:
        help_text += '- ' + choice + '<br />'

    return help_text
