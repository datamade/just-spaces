import csv
import sys

from django.conf import settings
# Set up a temporary settings file to ensure that we can import the pldp app
settings.configure(INSTALLED_APPS=['pldp'], USE_I18N=False)

from pldp import forms as pldp_forms

from fobi_custom.plugins.form_elements.fields.intercept import forms as plugin_forms


def display(choices, slug):
    """
    Get the display name for a form choice based on its slug. We need this function
    because we want to be able to store ACS data using the human-readable display
    name for each field, but in the code we want to reference the fields using their
    slugs, which are easier to change.

    :param choices: A list of tuples representing Django-style form choices.
    :param slug: The slug of the choice to select.
    :return: The display name for the given slug.
    """
    for choice_slug, display_name in choices:
        if choice_slug == slug:
            return display_name
    raise NameError('No choice for for slug {} in {}'.format(slug, str(choices)))


# Create mappings for compiled ACS tables based on the input variables that we can
# sum to generate those tables. For example, the value for `age_complex.under_5`
# is the sum of the ACS variables `male_under_5` and `female_under_5`.
FIELD_MAPPINGS = {
    # Ages don't need display names because their slugs are the same as their
    # human-readable names.
    'age_basic': {
        '0-14': [
            'male_under_5', 'male_5_to_9', 'male_10_to_14',
            'female_under_5', 'female_5_to_9', 'female_10_to_14',
        ],
        '15-24': [
            'male_15_to_17', 'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_15_to_17', 'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25-64': [
            'male_25_to_29', 'male_30_to_34', 'male_35_to_39', 'male_40_to_44',
            'male_45_to_49', 'male_50_to_54', 'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_25_to_29', 'female_30_to_34', 'female_35_to_39', 'female_40_to_44',
            'female_45_to_49', 'female_50_to_54', 'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
        '65+': [
            'male_65_to_66', 'male_67_to_69', 'male_70_to_74', 'male_75_to_79', 'male_80_to_84', 'male_85_plus',
            'female_65_to_66', 'female_67_to_69', 'female_70_to_74', 'female_75_to_79', 'female_80_to_84', 'female_85_plus',
        ]
    },
    'age_detailed': {
        '0-4': ['male_under_5', 'female_under_5'],
        '5-14': ['male_5_to_9', 'male_10_to_14', 'female_5_to_9', 'female_10_to_14'],
        '15-24': [
            'male_15_to_17', 'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_15_to_17', 'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25-44': [
            'male_25_to_29', 'male_30_to_34', 'male_35_to_39', 'male_40_to_44',
            'female_25_to_29', 'female_30_to_34', 'female_35_to_39', 'female_40_to_44',
        ],
        '45-64': [
            'male_45_to_49', 'male_50_to_54', 'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_45_to_49', 'female_50_to_54', 'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
        '65-74': [
            'male_65_to_66', 'male_67_to_69', 'male_70_to_74',
            'female_65_to_66', 'female_67_to_69', 'female_70_to_74',
        ],
        '75+': [
            'male_75_to_79', 'male_80_to_84', 'male_85_plus',
            'female_75_to_79', 'female_80_to_84', 'female_85_plus',
        ],
    },
    'age_complex': {
        '0-4': ['male_under_5', 'female_under_5'],
        '5-9': ['male_5_to_9', 'female_5_to_9'],
        '10-14': ['male_10_to_14', 'female_10_to_14'],
        '15-17': ['male_15_to_17', 'female_15_to_17'],
        '18-24': [
            'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25-34': ['male_25_to_29', 'male_30_to_34', 'female_25_to_29', 'female_30_to_34'],
        '35-44': ['male_35_to_39', 'male_40_to_44', 'female_35_to_39', 'female_40_to_44'],
        '45-54': ['male_45_to_49', 'male_50_to_54', 'female_45_to_49', 'female_50_to_54'],
        '55-64': [
            'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
        '65-74': [
            'male_65_to_66', 'male_67_to_69', 'male_70_to_74',
            'female_65_to_66', 'female_67_to_69', 'female_70_to_74',
        ],
        '75+': [
            'male_75_to_79', 'male_80_to_84', 'male_85_plus',
            'female_75_to_79', 'female_80_to_84', 'female_85_plus',
        ],
    },
    'gender_observational': {
        display(pldp_forms.GENDER_BASIC_CHOICES, 'male'): ['male_total'],
        display(pldp_forms.GENDER_BASIC_CHOICES, 'female'): ['female_total'],
        display(pldp_forms.GENDER_BASIC_CHOICES, 'unknown'): [],
    },
    'gender_intercept': {
        display(plugin_forms.GENDER_INTERCEPT_CHOICES, 'male'): ['male_total'],
        display(plugin_forms.GENDER_INTERCEPT_CHOICES, 'female'): ['female_total'],
        display(plugin_forms.GENDER_INTERCEPT_CHOICES, 'non_binary'): [],
        display(plugin_forms.GENDER_INTERCEPT_CHOICES, 'no_answer'): [],
    },
    'income': {
        display(plugin_forms.INCOME_CHOICES, 'under_20k'): ['under_10k', '10k_to_15k', '15k_to_20k'],
        display(plugin_forms.INCOME_CHOICES, '20_40k'): ['20k_to_25k', '25k_to_30k', '30k_to_35k', '35k_to_40k'],
        display(plugin_forms.INCOME_CHOICES, '40_60k'): ['40k_to_45k', '45k_to_50k', '50k_to_60k'],
        display(plugin_forms.INCOME_CHOICES, '60_75k'): ['60k_to_75k'],
        display(plugin_forms.INCOME_CHOICES, '75_100k'): ['75k_to_100k'],
        display(plugin_forms.INCOME_CHOICES, '100k_plus'): ['100k_to_125k', '125k_to_150k', '150k_to_200k', '200k_plus'],
    },
    'education': {
        display(plugin_forms.EDUCATION_CHOICES, 'no_high_school'): [
            'no_schooling', 'nursery', 'kindergarten', 'first_grade', 'second_grade',
            'third_grade', 'fourth_grade', 'fifth_grade', 'sixth_grade', 'seventh_grade',
            'eighth_grade', 'ninth_grade', 'tenth_grade', 'eleventh_grade', 'twelfth_grade',
        ],
        display(plugin_forms.EDUCATION_CHOICES, 'high_school'): [
            'high_school_diploma', 'ged', 'less_than_1_year_college',
            'one_or_more_years_college'
        ],
        display(plugin_forms.EDUCATION_CHOICES, 'associate'): ['associates'],
        display(plugin_forms.EDUCATION_CHOICES, 'bachelor'): ['bachelors'],
        display(plugin_forms.EDUCATION_CHOICES, 'graduate'): ['masters', 'professional', 'doctorate'],
    },
    'race': {
        display(plugin_forms.RACE_CHOICES, 'black'): ['black'],
        display(plugin_forms.RACE_CHOICES, 'asian'): ['asian'],
        display(plugin_forms.RACE_CHOICES, 'white'): ['white'],
        display(plugin_forms.RACE_CHOICES, 'hispanic_latino'): [],  # ACS doesn't include Hispanic as a race
        display(plugin_forms.RACE_CHOICES, 'native'): ['american_indian'],
        display(plugin_forms.RACE_CHOICES, 'hawaiian'): ['pacific_islander'],
        display(plugin_forms.RACE_CHOICES, 'multiple'): ['two_or_more'],
        display(plugin_forms.RACE_CHOICES, 'other'): ['other'],
    },
    'household_tenure': {
        # Household tenure is a free response intercept question, so it doesn't have
        # official choices in its form.
        '0-1979': ['owner_1979_or_earlier', 'renter_1979_or_earlier'],
        '1980-1989': ['owner_1980_to_1989', 'renter_1980_to_1989'],
        '1990-1999': ['owner_1990_to_1999', 'renter_1990_to_1999'],
        '2000-2009': ['owner_2000_to_2009', 'renter_2000_to_2009'],
        '2010-2014': ['owner_2010_to_2014', 'renter_2010_to_2014'],
        '2015+': ['owner_2015_plus', 'renter_2015_plus'],
    },
    'employment': {
        display(plugin_forms.EMPLOYMENT_CHOICES, 'employed'): ['employed'],
        display(plugin_forms.EMPLOYMENT_CHOICES, 'seeking'): ['unemployed'],
        display(plugin_forms.EMPLOYMENT_CHOICES, 'not_seeking'): ['not_in_labor_force'],
        display(plugin_forms.EMPLOYMENT_CHOICES, 'in_armed_forces'): ['in_armed_forces'],
    },
    'own_or_rent': {
        display(plugin_forms.OWN_OR_RENT_CHOICES, 'owner'): ['owner_total'],
        display(plugin_forms.OWN_OR_RENT_CHOICES, 'renter'): ['renter_total'],
        display(plugin_forms.OWN_OR_RENT_CHOICES, 'other'): [],
    },
    'transportation': {
        display(plugin_forms.TRANSPORTATION_CHOICES, 'walked'): ['walked'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'bicycle'): ['bicycle'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'car_truck_van'): ['car_truck_van'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'motorcycle'): ['motorcycle'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'train'): ['subway', 'railroad'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'bus'): ['bus'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'trolley'): ['trolley'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'ferryboat'): ['ferryboat'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'taxicab'): ['taxicab'],
        display(plugin_forms.TRANSPORTATION_CHOICES, 'other_means'): ['other_means'],
    },
}

if __name__ == '__main__':
    # Parse input files from the command line
    variable_name = sys.argv[1]
    if len(variable_name) == 0:
        raise NameError(
            'Script requires an argument representing the name of the output variable'
        )

    field_mapping = FIELD_MAPPINGS[variable_name]

    reader = csv.DictReader(sys.stdin)
    writer = csv.DictWriter(sys.stdout, fieldnames=['fips'] + list(field_mapping.keys()))
    writer.writeheader()

    for row in reader:
        output_row = {'fips': row['fips']}
        for output_field, input_fields in field_mapping.items():
            output_row[output_field] = 0
            for input_field in input_fields:
                output_row[output_field] += float(row[input_field])
        writer.writerow(output_row)
