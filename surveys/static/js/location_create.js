var typeDropdown = $("#id_location-geometry_type");

$(document).ready(function() {
  switchType();
});


typeDropdown.change(function() {
    switchType();
});


function switchType() {
  console.log("switch type function running...");
  var $locationArea = $('*[id^="div_id_location-area-"]');
  var $locationLine = $('*[id^="div_id_location-line-"]');

  var $locationLineDateMeasured = $('#id_location-line-date_measured');
  var $locationAreaDateMeasured = $('#id_location-area-date_measured');

  var selectedVal = typeDropdown[0].value;

  if (selectedVal == 'area') {
    console.log("area selected!");
    $locationLineDateMeasured.removeAttr('required');
    $locationAreaDateMeasured.prop('required', true);
    $locationLine.hide();
    $locationArea.show();
  } else if (selectedVal == 'line') {
    $locationAreaDateMeasured.removeAttr('required');
    $locationLineDateMeasured.prop('required', true);
    $locationArea.hide();
    $locationLine.show();
  } else {
    $locationAreaDateMeasured.removeAttr('required');
    $locationLineDateMeasured.removeAttr('required');
    $locationArea.hide();
    $locationLine.hide();
  }
}
