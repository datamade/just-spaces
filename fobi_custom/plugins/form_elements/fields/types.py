# Valid SurveyComponent types for the Data Analysis Designer (DAD). These are
# the UIDs of Fobi form elements that can sensibly be turned into charts.
# "Count" types represent a single value, and will be displayed as a median.
DAD_VALID_COUNT_TYPES = [
    'temperature_c', 'microclimate', 'decimal', 'float', 'integer'
]
# "Distribution" types represent a selection among multiple choices, and will
# be aggregated and displayed as percentiles.
DAD_VALID_DISTRIBUTION_TYPES = [
    'activity_observational', 'age_observational', 'gender_observational',
    'mode_observational', 'objects_observational', 'posture_observational',
    'education', 'employment', 'gender_intercept', 'income', 'own_or_rent',
    'race', 'transportation', 'boolean', 'null_boolean', 'radio', 'select',

]
# "Derived distribution" types represent a single value, but one that we want to
# bin and display as a distribution for the purpose of comparison to ACS data.
DAD_VALID_DERIVED_DISTRIBUTION_TYPES = [
    'age_intercept',
]
# All valid types merged into one list, for easy validation.
DAD_VALID_TYPES = (DAD_VALID_COUNT_TYPES + DAD_VALID_DISTRIBUTION_TYPES +
                   DAD_VALID_DERIVED_DISTRIBUTION_TYPES)
# All types that cannot be displayed as charts.
DAD_INVALID_TYPES = [
    'method', 'representation', 'time_character', 'time_start', 'time_stop',
    'total', 'help_text', 'checkbox_select_multiple', 'text', 'textarea', 'time'
]
