from fobi.utils import get_registered_form_element_plugins

# Valid SurveyComponent types for the Data Analysis Designer (DAD). These are
# the UIDs of Fobi form elements that can sensibly be turned into charts.

# "Count" types represent a single numeric value, and will be displayed as a median.
COUNT_TYPES = [
    'temperature_c', 'decimal', 'float', 'integer'
]
# "Observational" types represent counts for multiple choices, and will
# be aggregated and displayed as percentiles (a distribution).
OBSERVATIONAL_TYPES = [
    'age_observational', 'gender_observational', 'posture_observational', 'race_observational'
]
# "Observational count" types represent counts where each observed person can
# have one or more observation, meaning that we want to display the choices as
# raw counts.
OBSERVATIONAL_COUNT_TYPES = [
    'mode_observational', 'objects_observational', 'activity_observational',
]
# "Intercept" types represent one choice among multiple options selected by
# an interviewee. They will be aggregated and displayed as percentiles.
INTERCEPT_TYPES = [
    'education', 'employment', 'gender_intercept', 'income', 'own_or_rent',
    'race', 'transportation', 'boolean', 'null_boolean', 'radio', 'select',
]
# "Free response intercept" types are distinct from other intercept types in that
# they allow the user to freely respond with a numeric response to a question,
# which we can then bin and display as a distribution. Because the responses
# only store a number, we need to preset the boundaries of the bins.
FREE_RESPONSE_INTERCEPT_BINS = {
    'age_intercept': [5, 15, 25, 45, 65, 75],
    'household_tenure': [1980, 1990, 2000, 2010, 2015],
}
FREE_RESPONSE_INTERCEPT_TYPES = list(FREE_RESPONSE_INTERCEPT_BINS.keys())

ALL_TYPES = [plugin[0] for plugin in get_registered_form_element_plugins()]
# All valid types merged into one list, for easy validation.
ALL_VALID_TYPES = (COUNT_TYPES + OBSERVATIONAL_TYPES + OBSERVATIONAL_COUNT_TYPES +
                   INTERCEPT_TYPES + FREE_RESPONSE_INTERCEPT_TYPES)
# All types that cannot be displayed as charts.
ALL_INVALID_TYPES = list(set(ALL_TYPES) - set(ALL_VALID_TYPES))

# A list of types with their corresponding ACS variables.
TYPES_TO_ACS_VARIABLES = {
    'age_observational': {
        'basic': 'age_basic',
        'detailed': 'age_detailed',
        'complex': 'age_complex'
    },
    'gender_observational': {
        'basic': 'gender_observational',
    },
    'age_intercept': {
        'basic': 'age_detailed',
    },
    'gender_intercept': {
        'basic': 'gender_intercept',
    },
    'income': {
        'basic': 'income',
    },
    'education': {
        'basic': 'education',
    },
    'race': {
        'basic': 'race',
    },
    'race_observational': {
        'basic': 'race'
    },
    'employment': {
        'basic': 'employment',
    },
    'household_tenure': {
        'basic': 'household_tenure',
    },
    'own_or_rent': {
        'basic': 'own_or_rent',
    },
    'transportation': {
        'basic': 'transportation',
    },
}
