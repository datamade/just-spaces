GENDER_INTERCEPT_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('non_binary', 'Non-binary'),
    ('no_answer', 'Choose not to answer'),
]

INCOME_CHOICES = [
    ('under_20k', 'Less than $20,000 per year'),
    ('20_40k', '$20,000-$40,000 per year'),
    ('40_60k', '$40,000-$60,000 per year'),
    ('60_75k', '$60,000-$75,000 per year'),  # ACS breakpoint is $75k
    ('75_100k', '$75,000-$100,000 per year'),
    ('100k_plus', 'More than $100,000 per year'),
]

EDUCATION_CHOICES = [
    ('no_high_school', 'No high school diploma'),
    ('high_school', 'High school diploma'),
    ('associate', 'Associate\'s degree'),
    ('bachelor', 'Bachelor\'s degree'),
    ('graduate', 'Graduate/professional degree')
]

RACE_CHOICES = [
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
    ('employed', 'Employed'),
    ('seeking', 'Seeking work'),
    ('not_seeking', 'Not seeking work'),
    ('in_armed_forces', 'In the Armed Forces'),
]

OWN_OR_RENT_CHOICES = [
    ('owner', 'Homeowner'),
    ('renter', 'Renter'),
    ('other', 'Other'),
]

TRANSPORTATION_CHOICES = [
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
