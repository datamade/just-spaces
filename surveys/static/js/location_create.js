var location_area = $('*[id^="div_id_location-area-"]');
var location_line = $('*[id^="div_id_location-line-"]');

var location_line_date_measured = $('#id_location-line-date_measured');
var location_area_date_measured = $('#id_location-area-date_measured');

var typeDropdown = $("#id_location-geometry_type");


$(document).ready(function() {
  switchType(typeDropdown);
});


typeDropdown.change(function() {
    switchType(this);
});


function switchType(typeDropdown) {
  var selectedVal = typeDropdown.value

  if (selectedVal == 'area') {
    location_line_date_measured.removeAttr('required');
    location_area_date_measured.prop('required', true);
    location_line.hide();
    location_area.show();
  } else if (selectedVal == 'line') {
    location_area_date_measured.removeAttr('required');
    location_line_date_measured.prop('required', true);
    location_area.hide();
    location_line.show();
  } else {
    location_area_date_measured.removeAttr('required');
    location_line_date_measured.removeAttr('required');
    location_area.hide();
    location_line.hide();
  }
}
