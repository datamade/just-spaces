def choices_to_help_text(choices):
    help_text = ''
    for _, choice in choices:
        help_text += '- ' + choice + '<br />'

    return help_text


def choices_to_help_text_skip_first(choices):
    help_text = ''
    choices = choices[1:]

    for _, choice in choices:
        help_text += '- ' + choice + '<br />'

    return help_text
