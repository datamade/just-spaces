YEAR := 2017
COMPILE_ACS_DATA = cat $< | python3 scripts/compile_acs_data.py $(basename $(notdir $@)) > $@

.PHONY: all clean
all: final/acs/census_observations.csv final/shapefiles/cb_2018_42_bg_500k.shp

# Raw tables from the ACS API
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

# Intermediate compiled tables
INTERMEDIATE := intermediate/acs/age_basic.csv \
	intermediate/acs/age_detailed.csv \
	intermediate/acs/age_complex.csv \
	intermediate/acs/gender_observational.csv \
	intermediate/acs/gender_intercept.csv \
	intermediate/acs/education.csv \
	intermediate/acs/employment.csv \
	intermediate/acs/household_tenure.csv \
	intermediate/acs/race.csv \
	intermediate/acs/own_or_rent.csv \
	intermediate/acs/transportation.csv \
	intermediate/acs/income.csv

intermediate/acs/age_basic.csv: raw/acs/age_and_sex.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/age_detailed.csv: raw/acs/age_and_sex.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/age_complex.csv: raw/acs/age_and_sex.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/gender_observational.csv: raw/acs/age_and_sex.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/gender_intercept.csv: raw/acs/age_and_sex.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/education.csv: raw/acs/educational_attainment.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/household_tenure.csv: raw/acs/household_tenure.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/race.csv: raw/acs/race.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/own_or_rent.csv: raw/acs/household_tenure.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/transportation.csv: raw/acs/means_of_transit.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/income.csv: raw/acs/household_income.csv
	$(COMPILE_ACS_DATA)

intermediate/acs/employment.csv: raw/acs/employment_status.csv
	$(COMPILE_ACS_DATA)

clean:
	rm -Rf raw/acs/*.csv raw/shapefiles/*.zip intermediate/acs/*.csv final/acs/*.csv final/shapefiles/*

raw/acs/%.csv:
	python3 scripts/import_acs_data.py "$*" "${YEAR}" > "$@"

final/acs/census_observations.csv: ${INTERMEDIATE}
	python3 scripts/merge_acs_data.py $^ > $@

raw/shapefiles/cb_2018_42_bg_500k.zip:
	wget -O $@ https://www2.census.gov/geo/tiger/GENZ2018/shp/$(notdir $@)

intermediate/shapefiles/cb_2018_42_bg_500k.shp: raw/shapefiles/cb_2018_42_bg_500k.zip
	unzip "$<" -d $(dir $@)

final/shapefiles/cb_2018_42_bg_500k.shp: intermediate/shapefiles/cb_2018_42_bg_500k.shp
	ogr2ogr -dialect SQLite -sql "SELECT * FROM $(notdir $(basename $@)) WHERE COUNTYFP = '101'" $@ $<
