// Make sure JQuery is loaded
window.onload = function() {
  if (!window.jQuery) {
    throw new Error('JQuery must be loaded before charts.js');
  }
}

var ChartHelper = function(surveys, types, bins) {
  /**
   * Helper class for displaying HighCharts charts on a page.
   * This class depends on a number of nested objects as arguments in order to
   * sensibly initialize chart display. For an example of the structure of these
   * objects, see surveys.views.SurveySubmittedDetail.
   * @constructor
   * @param {Object} surveys - A data object containing survey results.
   * @param {Object} types - An object of type definitions for survey results.
   * @param {Object} bins - An object of bin definitions for binning survey results.
   */
  this.surveys = surveys;
  this.countTypes = types.count;
  this.observationalTypes = types.observational;
  this.interceptTypes = types.intercept;
  this.freeResponseInterceptTypes = types.freeResponseIntercept;
  this.freeResponseInterceptBins = bins.freeResponseIntercept;
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
  var isObservational = this.observationalTypes.indexOf(resultType) > -1;
  var isIntercept = this.interceptTypes.indexOf(resultType) > -1;
  var isFreeResponseIntercept = this.freeResponseInterceptTypes.indexOf(resultType) > -1;

  if (!(isCount || isObservational || isIntercept || isFreeResponseIntercept)) {
    // The data object needs to be one of the valid types
    throw new Error('Not a valid chart type: ' + resultType);
  } else {
    // Retrieve chart data depending on the data source type
    var chartData = {};
    var yAxisLabel = (isCount) ? 'Median response' : '% of responses';
    if (isCount) {
      chartData = this._getCountChartData(dataSourceId, chartTitle);
    } else if (isObservational) {
      chartData = this._getObservationalChartData(dataSourceId);
    } else if (isIntercept) {
      chartData = this._getInterceptChartData(dataSourceId);
    } else {
      chartData = this._getFreeResponseInterceptChartData(dataSourceId);
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
        text: yAxisLabel
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

ChartHelper.prototype._getObservationalChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "observational" type.
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
      chartData[key] = (countIsInitialized) ? chartData[key] + Number(savedData[key]) : Number(savedData[key]);
    });
  }
  return percentiles(chartData);
}

ChartHelper.prototype._getInterceptChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "intercept" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  var chartData = {};
  for (var i=0; i<this.surveys.length; i++) {
    var surveyResult = this.surveys[i].data[dataSourceId];
    try {
      var savedData = String(surveyResult.value);
    } catch(error) {
      alert('Object is not a valid String: ' + String(surveyResult.value));
      return;
    }
    var countIsInitialized = chartData.hasOwnProperty(savedData);
    // Count the appearances of each response
    chartData[savedData] = (countIsInitialized) ? chartData[savedData] + 1 : 1;
  }
  return percentiles(chartData);
}

ChartHelper.prototype._getFreeResponseInterceptChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "free response intercept" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
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
    // Bin the value according to the type of the response
    resultType = this.surveys[0].data[dataSourceId].type;
    var bins = this.freeResponseInterceptBins[resultType];
    if (bins === undefined) {
      throw new Error('No freeResponseInterceptBins found for type ' + resultType);
    }
    savedData = binValue(savedData, bins);
    // Initialize the chart data with empty values for each bin
    bins.forEach(function(bin, idx, arr) {
      // The binning function places values into bins by checking if the value
      // is strictly less than the bin. Since bin === bin, make each bin a hair
      // smaller so that it passes the check
      var downStep = (idx === 0) ? bin / 2 : (bin - arr[idx-1]) / 2;
      formattedBin = binValue(bin-downStep, arr);
      chartData[formattedBin] = 0;
    });
    // Add an extra bin value to make sure that the max gets displayed
    chartData[String(bins[bins.length-1]) + '+'] = 0;
    var countIsInitialized = chartData.hasOwnProperty(savedData);
    // Count the appearances of each response
    chartData[savedData] = (countIsInitialized) ? chartData[savedData] + 1 : 1;
  }
  return percentiles(chartData);
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

function percentiles(categories) {
  /**
   * Given an object of categories:counts, return percentiles for each category.
   * @param {Object} categories - An object of Numbers, each key representing a category.
   */
  // Get the total count over all categories
  var total = 0
  Object.keys(categories).forEach(function(key) {
    total += categories[key];
  });
  // Transform the summed object into percentiles
  var percentiles = {};
  Object.keys(categories).forEach(function(key) {
    percentiles[key] = categories[key] / total;
  });
  return percentiles;
}

function binValue(value, bins) {
  /**
   * Bucket a value according to a set of bins.
   * @param {Number} value - The value to bin.
   * @param {Array} bins - The bins to use for bucketing. The function assumes
   *                       that these bins are sorted in ascending order.
   */
  var binnedValue;
  for (var i=0; i<bins.length; i++) {
    var bin = bins[i];
    if (value < bin) {
      if (i === 0) {
        binnedValue = '<' + String(bin);
        break;
      } else if (i === bins.length-1) {
        binnedValue = String(bins[bins.length-1]) + '+';
        break;
      } else {
        var prevBin = bins[i-1];
        // Check if the bin represents a single integer instead of a range
        if (prevBin === bin-1) {
          binnedValue = String(bin);
        } else {
          binnedValue = String(prevBin) + '-' + String(bin-1);
        }
        break;
      }
    }
  }
  if (binnedValue === undefined) {
    // Value was larger than all bins
    debugger;
    binnedValue = String(bins[bins.length-1]) + '+';
  }
  return binnedValue;
}

