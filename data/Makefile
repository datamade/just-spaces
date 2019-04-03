YEAR := 2016

.PHONY: all clean rawacsdir
all: raw/acs/age_and_sex.csv \
	 raw/acs/household_income.csv

clean:
	rm -Rf raw/acs/*

rawacsdir:
	mkdir -p raw/acs

raw/acs/%.csv: rawacsdir
	python3 scripts/import_acs_data.py "$*" "${YEAR}" > "$@"
