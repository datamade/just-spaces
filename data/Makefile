YEAR := 2017

.PHONY: all clean
all: raw/acs/age_and_sex.csv \
	 raw/acs/household_income.csv \
	 raw/acs/employment_status.csv \
	 raw/acs/income_inequality.csv \
	 raw/acs/educational_attainment.csv \
	 raw/acs/means_of_transit.csv \
	 raw/acs/household_type.csv \
	 raw/acs/total_population.csv \
	 raw/acs/hours_worked_per_week.csv \
	 raw/acs/race.csv \
	 raw/acs/hispanic_or_latino_origin.csv \
	 raw/acs/household_tenure.csv \
	 raw/acs/vacancy_status.csv \
	 raw/acs/disability.csv

clean:
	rm -Rf raw/acs/*

raw/acs/%.csv:
	python3 scripts/import_acs_data.py "$*" "${YEAR}" > "$@"
