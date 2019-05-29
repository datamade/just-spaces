YEAR := 2017

.PHONY: all clean
all: final/acs/census_observations.csv

RAW := raw/acs/age_and_sex.csv \
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

intermediate/acs/gender.csv: raw/acs/age_and_sex.csv
	python3 scripts/variables/process_gender.py "$<" > "$@"

clean:
	rm -Rf raw/acs/*.csv final/*.csv

raw/acs/%.csv:
	python3 scripts/import_acs_data.py "$*" "${YEAR}" > "$@"

final/acs/census_observations.csv: ${RAW}
	python3 scripts/merge_acs_data.py $^ > $@

