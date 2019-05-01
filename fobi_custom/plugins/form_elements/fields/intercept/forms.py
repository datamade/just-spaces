GENDER_INTERCEPT_CHOICES = [
    ('', '-------'),
    ('male', 'Male'),
    ('female', 'Female'),
    ('non-binary', 'Non-binary'),
    ('no-answer', 'Choose not to answer'),
]

INCOME_CHOICES = [
    ('', '-------'),
    ('<20k', 'Less than $20,000 per year'),
    ('20-40k', '$20,000-$40,000 per year'),
    ('40-60k', '$40,000-$60,000 per year'),
    ('60-80k', '$60,000-$80,000 per year'),
    ('80-100k', '$80,000-$100,000 per year'),
    ('100k+', 'More than $100,000 per year'),
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
    ('walking', 'Walking'),
    ('bicycle', 'Bicycle'),
    ('car', 'Car'),
    ('train', 'Train'),
    ('bus', 'Bus'),
    ('rideshare', 'Rideshare'),
    ('other', 'Other'),
]
