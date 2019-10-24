.PHONY: shapefiles
shapefiles: final/shapefiles/cb_2018_42_bg_500k.shp

raw/shapefiles/%.zip:
	wget -O $@ https://www2.census.gov/geo/tiger/GENZ2018/shp/$(notdir $@)

intermediate/shapefiles/%.shp: raw/shapefiles/%.zip
	unzip "$<" -d $(dir $@)

final/shapefiles/%.shp: intermediate/shapefiles/%.shp
	ogr2ogr -dialect SQLite -sql "SELECT * FROM $(notdir $(basename $@)) WHERE COUNTYFP in $(COUNTIES)" $@ $<

final/shapefiles/cb_2018_42_bg_500k.shp: COUNTIES = ('101')
