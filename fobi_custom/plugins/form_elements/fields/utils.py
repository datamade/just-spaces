def choices_to_help_text(choices):
    help_text = ''
    for _, choice in choices:
        help_text += '- ' + choice + '<br />'

    return help_text
