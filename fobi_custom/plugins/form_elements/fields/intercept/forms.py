GENDER_INTERCEPT_CHOICES = [
    ('', '-------'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-binary'),
    ('no_answer', 'Choose not to answer'),
]

INCOME_CHOICES = [
    ('', '-------'),
    ('under_20k', 'Less than $20,000 per year'),
    ('_20_40k', '$20,000-$40,000 per year'),
    ('_40_60k', '$40,000-$60,000 per year'),
    ('_60_80k', '$60,000-$80,000 per year'),
    ('_80_100k', '$80,000-$100,000 per year'),
    ('_100k_plus', 'More than $100,000 per year'),
]

EDUCATION_CHOICES = [
    ('', '-------'),
    ('no_high_school', 'No high school diploma'),
    ('high_school', 'High school diploma'),
    ('associate', 'Associate\'s degree'),
    ('bachelor', 'Bachelor\'s degree'),
    ('graduate', 'Graduate/professional degree')
]

RACE_CHOICES = [
    ('', '-------'),
    ('black', 'African-American/Black'),
    ('asian', 'Asian'),
    ('white', 'White'),
    ('hispanic_latino', 'Hispanic or Latino'),
    ('native', 'Native American or Alaska Native'),
    ('hawaiian', 'Native Hawaiian or Pacific Islander'),
    ('multiple', 'Two or more races'),
    ('other', 'Other'),
]

EMPLOYMENT_CHOICES = [
    ('', '-------'),
    ('full_time', 'Working full-time'),
    ('part_time', 'Working part-time'),
    ('seeking', 'Seeking work'),
    ('not_seeking', 'Not seeking work'),
    ('student', 'Student'),
    ('homemaker', 'Homemaker'),
]

OWN_OR_RENT_CHOICES = [
    ('', '-------'),
    ('owner', 'Homeowner'),
    ('renter', 'Renter'),
    ('other', 'Other'),
]

TRANSPORTATION_CHOICES = [
    ('', '-------'),
    ('walked', 'Walked'),
    ('bicycle', 'Bicycle'),
    ('car_truck_van', 'Car, truck, or van'),
    ('motorcycle', 'Motorcycle'),
    ('train', 'Train'),
    ('bus', 'Bus'),
    ('trolley', 'Trolley'),
    ('ferryboat', 'Ferryboat'),
    ('taxicab', 'Taxicab or rideshare'),
    ('other_means', 'Other'),
]
