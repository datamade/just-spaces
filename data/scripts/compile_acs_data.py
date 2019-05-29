import csv
import sys

# Create mappings for compiled ACS tables based on the input variables that we can
# sum to generate those tables. For example, the value for `age_complex.under_5`
# is the sum of the ACS variables `male_under_5` and `female_under_5`.
FIELD_MAPPINGS = {
    'age_basic': {
        'under_14': [
            'male_under_5', 'male_5_to_9', 'male_10_to_14',
            'female_under_5', 'female_5_to_9', 'female_10_to_14',
        ],
        '15_to_24': [
            'male_15_to_17', 'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_15_to_17', 'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25_to_64': [
            'male_25_to_29', 'male_30_to_34', 'male_35_to_39', 'male_40_to_44',
            'male_45_to_49', 'male_50_to_54', 'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_25_to_29', 'female_30_to_34', 'female_35_to_39', 'female_40_to_44',
            'female_45_to_49', 'female_50_to_54', 'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
    },
    'age_detailed': {
        'under_5': ['male_under_5', 'female_under_5'],
        '5_to_14': ['male_5_to_9', 'male_10_to_14', 'female_5_to_9', 'female_10_to_14'],
        '15_to_24': [
            'male_15_to_17', 'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_15_to_17', 'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25_to_44': [
            'male_25_to_29', 'male_30_to_34', 'male_35_to_39', 'male_40_to_44',
            'female_25_to_29', 'female_30_to_34', 'female_35_to_39', 'female_40_to_44',
        ],
        '45_to_64': [
            'male_45_to_49', 'male_50_to_54', 'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_45_to_49', 'female_50_to_54', 'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
        '65_to_74': [
            'male_65_to_66', 'male_67_to_69', 'male_70_to_74',
            'female_65_to_66', 'female_67_to_69', 'female_70_to_74',
        ],
        '75_plus': [
            'male_75_to_79', 'male_80_to_84', 'male_85_plus',
            'female_75_to_79', 'female_80_to_84', 'female_85_plus',
        ],
    },
    'age_complex': {
        'under_5': ['male_under_5', 'female_under_5'],
        '5_to_9': ['male_5_to_9', 'female_5_to_9'],
        '10_to_14': ['male_10_to_14', 'female_10_to_14'],
        '15_to_17': ['male_15_to_17', 'female_15_to_17'],
        '18_to_24': [
            'male_18_to_19', 'male_20', 'male_21', 'male_22_to_24',
            'female_18_to_19', 'female_20', 'female_21', 'female_22_to_24',
        ],
        '25_to_34': ['male_25_to_29', 'male_30_to_34', 'female_25_to_29', 'female_30_to_34'],
        '35_to_44': ['male_35_to_39', 'male_40_to_44', 'female_35_to_39', 'female_40_to_44'],
        '45_to_54': ['male_45_to_49', 'male_50_to_54', 'female_45_to_49', 'female_50_to_54'],
        '55_to_64': [
            'male_55_to_59', 'male_60_to_61', 'male_62_to_64',
            'female_55_to_59', 'female_60_to_61', 'female_62_to_64',
        ],
        '65_to_74': [
            'male_65_to_66', 'male_67_to_69', 'male_70_to_74',
            'female_65_to_66', 'female_67_to_69', 'female_70_to_74',
        ],
        '75_plus': [
            'male_75_to_79', 'male_80_to_84', 'male_85_plus',
            'female_75_to_79', 'female_80_to_84', 'female_85_plus',
        ],
    },
    'gender_observational': {
        'male': ['male_total'],
        'female': ['female_total'],
        'unknown': [],
    },
    'gender_intercept': {
        'male': ['male_total'],
        'female': ['female_total'],
        'non_binary': [],
        'no_answer': [],
    },
    # TODO: Need to get a new variable here, for comparison
    'income': {
        'under_20k': [],
        '_20_40k': [],
        '_40_60k': [],
        '_60_80k': [],
        '_80_100k': [],
        '_100k_plus': [],
    },
    'education': {
        'no_high_school': [
            'no_schooling', 'nursery', 'kindergarten', 'first_grade', 'second_grade',
            'third_grade', 'fourth_grade', 'fifth_grade', 'sixth_grade', 'seventh_grade',
            'eighth_grade', 'ninth_grade', 'tenth_grade', 'eleventh_grade', 'twelfth_grade',
        ],
        'high_school': [
            'high_school_diploma', 'ged', 'less_than_1_year_college',
            'one_or_more_years_college'
        ],
        'associate': ['associates'],
        'bachelor': ['bachelors'],
        'graduate': ['masters', 'professional', 'doctorate'],
    },
    # TODO: Figure out hispanic/latino
    'race': {
        'black': ['black'],
        'asian': ['asian'],
        'white': ['white'],
        'hispanic_latino': [],
        'native': ['american_indian'],
        'hawaiian': ['pacific_islander'],
        'multiple': ['two_or_more'],
        'other': ['other'],
    },
    # TODO: Get a more granular source
    'employment': {
        'full_time': [],
        'part_time': [],
        'seeking': [],
        'not_seeking': [],
        'student': [],
        'homemaker': [],
    },
    'own_or_rent': {
        'owner': ['owner_total'],
        'renter': ['renter_total'],
        'other': [],
    },
    'transportation': {
        'walked': ['walked'],
        'bicycle': ['bicycle'],
        'car_truck_van': ['car_truck_van'],
        'motorcycle': ['motorcycle'],
        'train': ['subway', 'railroad'],
        'bus': ['bus'],
        'trolley': ['trolley'],
        'ferryboat': ['ferryboat'],
        'taxicab': ['taxicab'],
        'other_means': ['other_means'],
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
