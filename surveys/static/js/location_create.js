var location_area = $('*[id^="div_id_location-area-"]')
var location_line = $('*[id^="div_id_location-line-"]')

var location_line_date_measured = $('#id_location-line-date_measured')
var location_area_date_measured = $('#id_location-area-date_measured')

location_area.hide();
location_line.hide();

$("#id_location-geometry_type").change(function() {
    var selectedVal = this.value;

    if (selectedVal == 'area') {
      location_line_date_measured.removeAttr('required');
      location_area_date_measured.prop('required', true);
      location_line.hide();
      location_area.show();
    }

    if (selectedVal == 'line') {
      location_area_date_measured.removeAttr('required');
      location_line_date_measured.prop('required', true);
      location_area.hide();
      location_line.show();
    }
});
