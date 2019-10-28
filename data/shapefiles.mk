.PHONY: shapefiles
shapefiles: final/shapefiles/cb_2018_42_bg_500k.shp \
            final/shapefiles/cb_2018_39_bg_500k.shp \
            final/shapefiles/cb_2018_13_bg_500k.shp \
            final/shapefiles/cb_2018_25_bg_500k.shp \
            final/shapefiles/cb_2018_33_bg_500k.shp \
            final/shapefiles/cb_2018_37_bg_500k.shp \
            final/shapefiles/cb_2018_45_bg_500k.shp \
            final/shapefiles/cb_2018_17_bg_500k.shp \
            final/shapefiles/cb_2018_18_bg_500k.shp \
            final/shapefiles/cb_2018_55_bg_500k.shp

raw/shapefiles/cb_2018_%_bg_500k.zip:
	wget -O $@ https://www2.census.gov/geo/tiger/GENZ2018/shp/$(notdir $@)

intermediate/shapefiles/cb_2018_%_bg_500k.shp: raw/shapefiles/cb_2018_%_bg_500k.zip
	unzip "$<" -d $(dir $@)

final/shapefiles/cb_2018_%_bg_500k.shp: intermediate/shapefiles/cb_2018_%_bg_500k.shp
	COUNTIES=$$(./scripts/get_counties_for_state.py $(notdir $*)) && \
	    ogr2ogr -dialect SQLite -sql "SELECT * FROM $(notdir $(basename $@)) WHERE COUNTYFP in $$COUNTIES" $@ $<
