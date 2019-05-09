# Valid SurveyComponent types for the Data Analysis Designer (DAD). These are
# the UIDs of Fobi form elements that can sensibly be turned into charts.

# "Count" types represent a single numeric value, and will be displayed as a median.
COUNT_TYPES = [
    'temperature_c', 'decimal', 'float', 'integer'
]
# "Observational" types represent counts for multiple choices, and will
# be aggregated and displayed as percentiles (a distribution).
OBSERVATIONAL_TYPES = [
    'activity_observational', 'age_observational', 'gender_observational',
    'mode_observational', 'objects_observational', 'posture_observational',
]
# "Intercept" types represent one choice among multiple options selected by
# an interviewee. They will be aggregated and displayed as percentiles.
INTERCEPT_TYPES = [
    'education', 'employment', 'gender_intercept', 'income', 'own_or_rent',
    'race', 'transportation', 'boolean', 'null_boolean', 'radio', 'select',
]
# "Free response intercept" types are distinct from other intercept types in that
# they allow the user to freely respond with a numeric response to a question,
# which we can then bin and display as a distribution.
FREE_RESPONSE_INTERCEPT_TYPES = [
    'age_intercept', 'household_tenure'
]
# All valid types merged into one list, for easy validation.
ALL_VALID_TYPES = (COUNT_TYPES + OBSERVATIONAL_TYPES + INTERCEPT_TYPES +
                   FREE_RESPONSE_INTERCEPT_TYPES)
# All types that cannot be displayed as charts.
ALL_INVALID_TYPES = [
    'method', 'representation', 'time_character', 'time_start', 'time_stop',
    'total', 'help_text', 'checkbox_select_multiple', 'text', 'textarea', 'time',
    'microclimate',
]
