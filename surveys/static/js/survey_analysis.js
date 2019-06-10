$(document).ready(function () {
  var table = $('#survey-submitted-detail').DataTable({
    buttons: [{
      extend: 'csv',
      text: '<i class="fas fa-sm fa-arrow-alt-circle-down mr-2"></i>Download as CSV',
      title: '{{ form_entry.name }}'
    }],
    lengthChange: false,
  });

  table.buttons().container()
      .appendTo( '#survey-submitted-detail_wrapper .col-md-6:eq(0)' );

  // Helpful JQuery selectors
  var $totalForms = $('[name$=TOTAL_FORMS]');
  var chartContainer = '[class^="chart-container-"]';
  var censusContainer = 'tr[id$="-container-census_areas"]';
  var censusSelectBox = 'select[id$="-census_areas"]';

  // Load the ChartHelper from charts.js
  var surveys = JSON.parse('{{ surveys_submitted_json | escapejs }}');
  var types = JSON.parse('{{ types | escapejs }}');
  var bins = JSON.parse('{{ bins | escapejs }}');
  var choices = JSON.parse('{{ choices | escapejs }}');
  charts = new ChartHelper(surveys, types, bins, choices);

  // Load ACS variable map for Fobi types
  var acsCompatibleTypes = JSON.parse('{{ acs_compatible_types | escapejs }}');

  function resetChartOrder() {
    // Update the 'order' field of each chart on the page to match its visual
    // order in the list of charts
    $(chartContainer).find('input[name$="order"]').each(function(idx) {
      // Skip the empty form, whose name contains the string __prefix__
      if (this.name.indexOf('__prefix__') === -1) {
        formIdx = idx + 1;  // Form order values are 1-indexed
        $(this).val(formIdx);
      }
    });
  }

  function toggleMoveButtonVisibility() {
    // Check to see if there is only one chart on the page, and if there is, hide
    // the move buttons on that chart
    var $visibleCharts = $(chartContainer).filter(':visible');
    var numVisibleCharts = $visibleCharts.length;
    if (numVisibleCharts > 0) {
      if (numVisibleCharts === 1) {
        $('.move-chart-up,.move-chart-down').hide();
      } else {
        $('.move-chart-up,.move-chart-down').show();
        // Hide the up/down buttons for the first and last charts on the page
        $visibleCharts.first().find('.move-chart-up').hide();
        $visibleCharts.last().find('.move-chart-down').hide();
      }
    }
  }
  toggleMoveButtonVisibility();

  function toggleCensusContainerVisibility($censusContainer, dataSourceId) {
    /**
     * Check to see whether a data source can be compared to ACS data, and if it
     * can, show its corresponding Census selectbox.
     *
     * @param {Object} $censusContainer - A JQuery object representing the container to toggle.
     * @param {String} dataSourceId - The ID of the data source in question.
     */
    var sourceType = surveys[0].data[dataSourceId].type;
    var isAcsCompatibleType = false;
    for (var i=0; i<acsCompatibleTypes.length; i++) {
      if (sourceType === acsCompatibleTypes[i]) {
        isAcsCompatibleType = true;
        break;
      }
    }
    if (isAcsCompatibleType) {
      $censusContainer.show();
    } else {
      $censusContainer.hide();
    }
  }
  // On first page load, toggle the Census select box visibility for any visible
  // charts
  $(chartContainer).filter(':visible').find(censusContainer).each(function() {
    var $dataSourceSelect = $(this).parents(chartContainer).find('select[name$="-primary_source"]');
    if ($dataSourceSelect.length > 0) {
      var dataSourceId = $dataSourceSelect.val();
      toggleCensusContainerVisibility($(this), dataSourceId);
    }
  });

  // Initialize sortable chart widgets
  $('#sortable-chart-container').sortable({
    handle: ".portlet-handle",
    stop: resetChartOrder,
  });

  $('#add-new-chart').click(function() {
    var formIdx = $totalForms.val();
    $('#sortable-chart-container').append($('#chart-formset-template').html().replace(/__prefix__/g, formIdx));
    $totalForms.val(parseInt(formIdx) + 1);
    resetChartOrder();
    toggleMoveButtonVisibility();
  });

  $('form').on('click', '.delete-chart', function(event) {
    // Use the handler syntax .on('click', elem, fn) in order to make sure that the
    // handler is fired for events that did not exist when the page was loaded,
    // namely new charts
    event.preventDefault();
    $(this).parents(chartContainer).hide();
    $(this).parents(chartContainer).find('input[name$="DELETE"]').prop("checked", "true");
    toggleMoveButtonVisibility();
  });

  $('form').on('click', '.move-chart-up', function(event) {
    event.preventDefault();
    var $parentContainer = $(this).parents(chartContainer);
    // Move parent container up one step
    if ($parentContainer.not(':first-child')) {
      $parentContainer.prev().before($parentContainer);
    }
    resetChartOrder();
    toggleMoveButtonVisibility();
  });

  $('form').on('click', '.move-chart-down', function(event) {
    event.preventDefault();
    var $parentContainer = $(this).parents(chartContainer);
    // Move parent container down one step
    if ($parentContainer.not(':last-child')) {
      $parentContainer.next().after($parentContainer);
    }
    resetChartOrder();
    toggleMoveButtonVisibility();
  });

  $('form').on('change', 'select[name$="-primary_source"]', function(event) {
    // Listen to the primary data source select box, and update charts and
    // other form options when the data source changes
    var dataSourceId = $(this).val();
    var $container = $(this).parents(chartContainer);
    var chartId = $container.find('.highcharts-chart').first().attr('id');
    var $censusContainer = $container.find(censusContainer).first();
    var $censusSelect = $container.find(censusSelectBox).first();

    if (dataSourceId === '') {
      // User selected the null option, so remove the chart
      charts.destroyChart(chartId);
      // Clear and hide conditional inputs
      $censusContainer.hide();
      $censusSelect.val([]);
    } else {
      // Show the chart
      var chartTitle = $(this).find('option:selected').html();
      charts.loadChart(chartId, chartTitle, dataSourceId);
      // Show conditional inputs
      toggleCensusContainerVisibility($censusContainer, dataSourceId);
    }
  });

  $('form').on('change', censusSelectBox, function(event) {
    // Listen to ACS data source multiselect boxes, and update the charts when the
    // data source changes
    var primarySourceId = $(this).parents(chartContainer).find('select[name$="primary_source"]').val();
    var chartId = $(this).parents(chartContainer).find('.highcharts-chart').first().attr('id');
    charts.removeAllAcsSeries(chartId);

    var geographies = $(this).find('option:selected').map(function() {
      return {id: $(this).val(), label: $(this).text()};
    });
    if (geographies.length > 0) {
      for (var i=0; i<geographies.length; i++) {
        var geography = geographies[i];
        var dataUrl = "{% url 'acs' %}?census_area=" + geography.id + "&primary_source=" + primarySourceId;
        // Since the following code executes asynchronously, wrap it in an immediately
        // executed function in order to ensure that the proper geography label is
        // applied. See: https://stackoverflow.com/a/15347771
        (function(geographyLabel) {
          $.getJSON(dataUrl).done(function(acsData) {
            charts.addAcsSeries(chartId, acsData, geographyLabel);
          }).fail(function(jqxhr, textStatus, error) {
            var err = textStatus + ", " + error;
            console.log("Request to " + dataUrl + " failed: " + err);
          });
        })(geography.label);
      }
    }
  });

  // Load visible charts
  $(chartContainer).filter(':visible').find('select[name$="primary_source"]').each(function() {
    var dataSourceId = $(this).val();
    var chartId = $(this).parents(chartContainer).find('.highcharts-chart').first().attr('id');
    if (dataSourceId != '') {
      var chartTitle = $(this).find('option:selected').html();
      charts.loadChart(chartId, chartTitle, dataSourceId);
    }
  });

  $('#clear-charts').click(function() {
    $('#chart-formset').find(chartContainer).find('.delete-chart').click();
  });

  $('#save-charts').click(function() {
    $('#chart-formset').submit();
  });

} );
