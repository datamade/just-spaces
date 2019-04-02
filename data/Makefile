PA_FIPS := 42
PHILLY_FIPS := 101

.PHONY: all clean
all: raw/acs/age_and_sex.csv \
	 raw/acs/household_income.csv

clean:
	rm -Rf raw/acs/*

raw/acs/%.csv:
	python3 scripts/import_acs_data.py "$*" > "$@"
