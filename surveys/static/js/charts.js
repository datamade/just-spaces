// Make sure JQuery is installed
window.onload = function() {
  if (!window.jQuery) {
    throw new Error('JQuery must be loaded before charts.js');
  }
}

var ChartHelper = function(surveys, types) {
  /**
   * Helper class for displaying HighCharts charts on a page.
   *
   * @constructor
   * @param {Object} surveys - A data object containing survey results.
   * @param {Object} types - An object of type definitions.
   */
  this.surveys = surveys;
  this.countTypes = types.countTypes;
  this.distributionTypes = types.distributionTypes;
  this.derivedDistributionTypes = types.derivedDistributionTypes;
}

ChartHelper.prototype.loadChart = function(chartId, chartTitle, dataSourceId) {
  /**
   * Load a Highcharts chart.
   * @param {String} chartId - The ID attribute of the chart container on the page.
   * @param {String} chartTitle - The title of the chart to display.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  // Check the type of the result to determine what kind of chart to display
  var resultType;
  if (this.surveys.length === 0) {
    throw new Error('This survey has no collected data.');
  } else {
    resultType = this.surveys[0].data[dataSourceId].type;
  }
  var isCount = this.countTypes.indexOf(resultType) > -1;
  var isDistribution = this.distributionTypes.indexOf(resultType) > -1;
  var isDerivedDistribution = this.derivedDistributionTypes.indexOf(resultType) > -1;
  // Retrieve chart data depending on the data source type
  var chartData = {};
  if (!(isCount || isDistribution || isDerivedDistribution)) {
    // The data object needs to be one of the valid types
    throw new Error('Not a valid chart type: ' + resultType);
  } else {
    if (isCount) {
      chartData = this._getCountChartData(dataSourceId, chartTitle);
    } else if (isDistribution) {
      chartData = this._getDistributionChartData(dataSourceId);
    } else {
      chartData = this._getDerivedDistributionChartData(dataSourceId);
    }
  }
  // Format the chart data for Highcharts display
  var categories = [];
  var series = [{
    data: []
  }];
  Object.keys(chartData).forEach(function(key) {
    categories.push(key);
    series[0].data.push(chartData[key]);
  });
  // Initialize a Highcharts chart
  Highcharts.chart(chartId, {
    chart: {
      type: 'column',
      backgroundColor: '#FFFFFF',
      shadow: true
    },
    title: {
      text: chartTitle
    },
    xAxis: {
      categories: categories,
    },
    yAxis: {
      title: {
        text: chartTitle
      }
    },
    legend: {
      enabled: false
    },
    series: series
  });
}

ChartHelper.prototype._getCountChartData = function(dataSourceId, chartTitle) {
  /**
   * Get chart data for a chart of the "count" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   * @param {String} chartTitle - The title of the chart to display.
   */
  var chartData = {};
  for (var i=0; i<this.surveys.length; i++) {
    var surveyResult = this.surveys[i].data[dataSourceId];
    try {
      var savedData = Number(surveyResult.value);
    } catch(error) {
      alert('Object is not a valid Number: ' + String(surveyResult.value));
      return;
    }
    var countIsInitialized = chartData.hasOwnProperty(chartTitle);
    chartData[chartTitle] = (countIsInitialized) ? chartData[chartTitle].concat([savedData]) : [savedData];
  }
  var cleanedData = {};
  Object.keys(chartData).forEach(function(key) {
    cleanedData[key] = median(chartData[key]);
  });
  return cleanedData;
}

ChartHelper.prototype._getDistributionChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "distribution" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  var chartData = {};
  for (var i=0; i<this.surveys.length; i++) {
    var surveyResult = this.surveys[i].data[dataSourceId];
    try {
      var savedData = JSON.parse(surveyResult.value);
    } catch(error) {
      alert('Object is not valid JSON: ' + String(surveyResult.value));
      return;
    }
    Object.keys(savedData).forEach(function(key) {
      var countIsInitialized = chartData.hasOwnProperty(key);
      chartData[key] = (countIsInitialized) ? chartData[key].concat([savedData[key]]) : [savedData[key]];
    });
  }
  return percentiles(chartData);
}

ChartHelper.prototype._getDerivedDistributionChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "derived distribution" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  var chartData = {};
  return chartData;
}

ChartHelper.prototype.destroyChart = function(chartId) {
  /**
   * Destroy a Highcharts chart.
   * @param {String} chartId - The ID attribute of the chart container on the page.
   */
  var chart = $('#' + chartId).highcharts();
  chart.destroy();
}

function median(numArr) {
  /**
   * Given an array of numbers, return the median.
   * Algorithm adapted from Harry Stevens' code on StackOverflow:
   * https://stackoverflow.com/a/39639518
   * @param {Number} numArr - An array of numbers.
   */
  numArr.sort(function(a, b){ return a - b; });
  var i = numArr.length / 2;
  return i % 1 == 0 ? (numArr[i - 1] + numArr[i]) / 2 : numArr[Math.floor(i)];
}

function percentiles(arrOb) {
  /**
   * Given an object of arrays, return percentiles for each key.
   * @param {Object} arrOb - An object of arrays, each key representing a category.
   */
  // Sum category arrays to return a count for each category
  var sums = {};
  Object.keys(arrOb).forEach(function(key) {
    sum = 0;
    arrOb[key].forEach(function(val) {
      sum += val;
    });
    sums[key] = sum;
  });
  // Get the total count over all categories
  var total = 0
  Object.keys(sums).forEach(function(key) {
    total += sums[key];
  });
  // Transform the summed object into percentiles
  var percentiles = {};
  Object.keys(sums).forEach(function(key) {
    percentiles[key] = sums[key] / total;
  });
  return percentiles;
}
