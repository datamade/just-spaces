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
    var chartData = [];
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
  chartData.forEach(function(data) {
    // chartData elements are stored as an Array where the first element is the
    // category name and the second element is the value -- a map would be easier
    // to work with, but wouldn't preserve the order of the categories
    var category = data[0];
    var value = data[1];
    categories.push(category);
    series[0].data.push(value);
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

ChartHelper.prototype._getChartData = function(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc) {
  /**
   * Base function for retrieving survey data for display on a chart.
   * This function takes a number of transformation functions as arguments and
   * applies them to the selected survey data. For an example of how it is used,
   * see the _getCountChartData method.
   * @param {String} dataSourceId - The ID of the primary data source to retrieve.
   * @param {Function} initChartDataFunc - A function that takes no arguments
   *                                       and returns the initialized chartData
   *                                       object.
   * @param {Function} castFunc - A function that takes as an argument the survey
   *                              data value and casts it to the appropriate type.
   * @param {Function} updateChartDataFunc - A function that takes as arguments the
   *                                         initialized chartData object and the
   *                                         formatted survey data value and updates
   *                                         the chartData object accordingly.
   * @param {Function} aggFunc - A function that takes as an argument the updated
   *                             chartData object and aggregates across its values
   *                             (e.g. returning the median value for each key)
   */
  var chartData = initChartDataFunc();
  for (var i=0; i<this.surveys.length; i++) {
    var surveyResult = this.surveys[i].data[dataSourceId];
    try {
      // Cast the saved value to the appropriate type
      var savedData = castFunc(surveyResult.value);
    } catch(error) {
      var funcName = castFunc.name ? castFunc.name : String(castFunc);
      throw new Error('Object cannot be cast by ' + funcName + ': ' + String(surveyResult.value));
    }
    updateChartDataFunc(chartData, savedData);
  }
  return aggFunc(chartData);
}

ChartHelper.prototype._getCountChartData = function(dataSourceId, chartTitle) {
  /**
   * Get chart data for a chart of the "count" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   * @param {String} chartTitle - The title of the chart to display.
   */
  function initChartDataFunc() { return []};
  var castFunc = Number;
  function updateChartDataFunc(chartData, savedData) {
    var categoryFound = false;
    // If an entry for this category exists in the chartData array, append the
    // new value to its array
    for (var i=0; i<chartData.length; i++) {
      var categoryName = chartData[i][0];
      if (categoryName === chartTitle) {
        chartData[i][1].push(savedData);
        categoryFound = true;
        break;
      }
    }
    if (!categoryFound) {
      // Insert an entry for this count in the chartData array
      chartData.push([chartTitle, [savedData]]);
    }
  }
  var aggFunc = medians;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype._getObservationalChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "observational" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  function initChartDataFunc() { return []};
  var castFunc = JSON.parse;
  function updateChartDataFunc(chartData, savedData) {
    Object.keys(savedData).forEach(function(key) {
      var categoryFound = false;
      var savedDataValue = Number(savedData[key]);
      // If an entry for this category exists in the chartData array, inncrement
      // its counter
      for (var i=0; i<chartData.length; i++) {
        var categoryName = chartData[i][0];
        if (categoryName === key) {
          chartData[i][1] += savedDataValue;
          categoryFound = true;
          break;
        }
      }
      if (!categoryFound) {
        // Insert an entry for this count in the chartData array
        chartData.push([key, savedDataValue]);
      }
    });
  }
  var aggFunc = percentiles;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype._getInterceptChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "intercept" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  function initChartDataFunc() { return []};
  var castFunc = String;
  function updateChartDataFunc(chartData, savedData) {
    var categoryFound = false;
    // If an entry for this category exists in the chartData array, increment its counter
    for (var i=0; i<chartData.length; i++) {
      var categoryName = chartData[i][0];
      if (categoryName === savedData) {
        chartData[i][1] += 1;
        categoryFound = true;
        break;
      }
    }
    if (!categoryFound) {
      // Insert an entry for this count in the chartData array
      chartData.push([savedData, 1]);
    }
  }
  var aggFunc = percentiles;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype._getFreeResponseInterceptChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "free response intercept" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  var resultType = this.surveys[0].data[dataSourceId].type;
  var bins = this.freeResponseInterceptBins[resultType];
  if (bins === undefined) {
    throw new Error('No freeResponseInterceptBins found for type ' + resultType);
  }
  function initChartDataFunc() {
    var chartData = [];
    // Initialize the chart data with empty values for each bin
    bins.forEach(function(bin, idx, arr) {
      // The binning function places values into bins by checking if the value
      // is strictly less than the bin. Since bin === bin, make each bin a hair
      // smaller so that it passes the check
      var downStep = (idx === 0) ? bin / 2 : (bin - arr[idx-1]) / 2;
      formattedBin = binValue(bin-downStep, arr);
      chartData.push([formattedBin, 0]);
    });
    // Add an extra bin value to make sure that the max gets displayed
    chartData.push([String(bins[bins.length-1]) + '+', 0]);
    return chartData;
  };
  var castFunc = Number;
  function updateChartDataFunc(chartData, savedData) {
    // Bin the value according to the type of the response
    savedData = binValue(savedData, bins);
    chartData.forEach(function(category, idx, arr) {
      var categoryName = category[0];
      if (categoryName === savedData) {
        arr[idx][1] += 1;
      }
    });
  }
  var aggFunc = percentiles;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype.destroyChart = function(chartId) {
  /**
   * Destroy a Highcharts chart.
   * @param {String} chartId - The ID attribute of the chart container on the page.
   */
  var chart = $('#' + chartId).highcharts();
  chart.destroy();
}

function medians(categories) {
  /**
   * Given an array map of categories and numbers, return the median number for
   * each category in the array.
   * Algorithm adapted from Harry Stevens' code on StackOverflow:
   * https://stackoverflow.com/a/39639518
   * @param {Array} categories - A nested set of arrays acting as a Map, where
   *                             the first element represents a category name and the
   *                             second element is an array of numbers representing
   *                             all recorded values for that category.
   */
  return categories.map(function(category) {
    var categoryName = category[0];
    var numArr = category[1];
    numArr.sort(function(a, b) { return a - b; });
    var i = numArr.length / 2;
    return [categoryName, i % 1 == 0 ? (numArr[i - 1] + numArr[i]) / 2 : numArr[Math.floor(i)]];
  });
}

function percentiles(categories) {
  /**
   * Given an array map of categories:counts, return percentiles for each category.
   * @param {Array} categories - A nested array of numbers acting as a Map, where
   *                             the first element represents a category name and the
   *                             second element represents its value.
   */
  var total = categories.reduce(function(acc, category) { return acc + category[1] }, 0);
  return categories.map(function(category) { return [category[0], category[1] / total]})
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
    binnedValue = String(bins[bins.length-1]) + '+';
  }
  return binnedValue;
}
