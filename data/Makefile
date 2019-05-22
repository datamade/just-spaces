YEAR := 2017

.PHONY: all clean
all: final/acs/age_and_sex.csv \
	 final/acs/household_income.csv \
	 final/acs/employment_status.csv \
	 final/acs/income_inequality.csv \
	 final/acs/educational_attainment.csv \
	 final/acs/means_of_transit.csv \
	 final/acs/household_type.csv \
	 final/acs/total_population.csv \
	 final/acs/hours_worked_per_week.csv \
	 final/acs/race.csv \
	 final/acs/hispanic_or_latino_origin.csv \
	 final/acs/household_tenure.csv \
	 final/acs/vacancy_status.csv \
	 final/acs/disability.csv

clean:
	rm -Rf raw/acs/*

raw/acs/%.csv:
	python3 scripts/import_acs_data.py "$*" "${YEAR}" > "$@"

# Eventually we may want to do more transformation on these files. For now,
# simply copy them over
final/acs/%.csv: raw/acs/%.csv
	cp "$<" "$@"
