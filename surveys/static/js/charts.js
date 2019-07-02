// Make sure JQuery is loaded
window.onload = function() {
  if (!window.jQuery) {
    throw new Error('JQuery must be loaded before charts.js');
  }
}

var ChartHelper = function(surveys, types, bins, choices) {
  /**
   * Helper class for displaying HighCharts charts on a page.
   * This class depends on a number of nested objects as arguments in order to
   * sensibly initialize chart display. For an example of the structure of these
   * objects, see surveys.views.SurveySubmittedDetail.
   * @constructor
   * @param {Object} surveys - A data object containing survey results.
   * @param {Object} types - An object of type definitions for survey results.
   * @param {Object} bins - An object of bin definitions for binning survey results.
   * @param {Object} choices - An object of choices for different questions, indexed
   *                           by plugin UID (AKA type).
   */
  this.surveys = surveys;
  this.types = types;
  this.bins = bins;
  this.choices = choices;
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

  var isCount = this.types.count.indexOf(resultType) > -1;
  var isObservational = this.types.observational.indexOf(resultType) > -1;
  var isObservationalCount = this.types.observationalCount.indexOf(resultType) > -1;
  var isIntercept = this.types.intercept.indexOf(resultType) > -1;
  var isFreeResponseIntercept = this.types.freeResponseIntercept.indexOf(resultType) > -1;

  if (!(isCount || isObservational || isObservationalCount || isIntercept || isFreeResponseIntercept)) {
    // The data object needs to be one of the valid types
    throw new Error('Not a valid chart type: ' + resultType);
  } else {
    // Retrieve chart data depending on the data source type
    var chartData = [];
    if (isCount) {
      chartData = this._getCountChartData(dataSourceId, chartTitle);
    } else if (isObservational) {
      chartData = this._getObservationalChartData(dataSourceId);
    } else if (isObservationalCount) {
      // Return chart data as raw counts
      chartData = this._getObservationalChartData(dataSourceId, true);
    } else if (isIntercept) {
      chartData = this._getInterceptChartData(dataSourceId);
    } else {
      chartData = this._getFreeResponseInterceptChartData(dataSourceId);
    }
  }
  // Format the chart data for Highcharts display
  var categories = [];
  var series = [{
    name: this.getSeriesName(),
    data: [],
    color: '#a1bfa2',
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
  // Get chart options based on the data source type
  var yAxisLabel = '';
  if (isCount) {
    if (this.surveys.length >= 5) {
      yAxisLabel = 'Response';
    } else {
      yAxisLabel = 'Median response';
    }
  } else if (isObservationalCount) {
    yAxisLabel = 'Number of responses';
  } else {
    yAxisLabel = '% of responses';
  }
  var chartType = (isCount && this.surveys.length >= 5) ? 'boxplot' : 'column';
  var ACSColors = [
    '#ffd700',
    '#ffb14e',
    '#fa8775',
    '#eb549e',
    '#e94e0c',
    '#cd58bb',
    '#9e86d7',
    '#015c75',
    '#cde8ce',
    '#d6edf4'
  ]

  shuffle(ACSColors);

  // Initialize a Highcharts chart
  Highcharts.chart(chartId, {
    chart: {
      type: chartType,
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
      enabled: true
    },
    series: series,
    colors: ACSColors
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
  for (var i = 0; i < this.surveys.length; i++) {
    var surveyResult = this.surveys[i].data[dataSourceId];
    try {
      // Cast the saved value to the appropriate type
      var savedData = castFunc(surveyResult.value);
    } catch (error) {
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
  function initChartDataFunc() { return [] };
  var castFunc = Number;
  function updateChartDataFunc(chartData, savedData) {
    var categoryFound = false;
    // If an entry for this category exists in the chartData array, append the
    // new value to its array
    for (var i = 0; i < chartData.length; i++) {
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
  var aggFunc = (this.surveys.length >= 5) ? quintiles : medians;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype._getObservationalChartData = function(dataSourceId, isCount) {
  /**
   * Get chart data for a chart of the "observational" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   * @param {Boolean} isCount - Whether or not to show raw counts in the chart.
   */
  var choices = this.choices;  // Extract from 'this' so we can use the choices in the following func.
  function initChartDataFunc() {
    // Initialize all possible values with a count of 0
     var dataSourceChoices = choices[dataSourceId];
     var chartData = [];
     for (var i=0; i<dataSourceChoices.length; i++) {
      chartData.push([dataSourceChoices[i][1], 0]);
     }
     return chartData;
  };
  function castFunc(value) {
    // Cast choices to their human-readable equivalent
    var dataSourceChoices = choices[dataSourceId];
    // Observational data are stored in a JSON blob, so iterate its attributes and
    // convert them to human-readable format
    var parsedValue = JSON.parse(value);
    var humanReadableValue = {};
    Object.keys(parsedValue).forEach(function(key, idx) {
      for (var i=0; i<dataSourceChoices.length; i++) {
        var choice = dataSourceChoices[i][0];
        if (key === choice) {
          humanReadableValue[dataSourceChoices[i][1]] = parsedValue[key];
          break;
        }
      }
    });
    return humanReadableValue;
  };
  function updateChartDataFunc(chartData, savedData) {
    Object.keys(savedData).forEach(function(key) {
      var categoryFound = false;
      var savedDataValue = Number(savedData[key]);
      // If an entry for this category exists in the chartData array, increment
      // its counter
      for (var i = 0; i < chartData.length; i++) {
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
  var aggFunc = (isCount) ? function(categories) { return categories; } : percentiles;
  return this._getChartData(dataSourceId, initChartDataFunc, castFunc, updateChartDataFunc, aggFunc);
}

ChartHelper.prototype._getInterceptChartData = function(dataSourceId) {
  /**
   * Get chart data for a chart of the "intercept" type.
   * @param {String} dataSourceId - The ID of the primary data source to display.
   */
  var choices = this.choices;  // Extract from 'this' so we can use the choices in the following func.
  function initChartDataFunc() {
    // Initialize all possible values with a count of 0
     var dataSourceChoices = choices[dataSourceId];
     var chartData = [];
     for (var i=0; i<dataSourceChoices.length; i++) {
      chartData.push([dataSourceChoices[i][1], 0]);
     }
     return chartData;
  };
  function castFunc(value) {
    // Cast choices to their human-readable equivalent
    var dataSourceChoices = choices[dataSourceId];
    var humanReadableValue = '';
    for (var i=0; i<dataSourceChoices.length; i++) {
      var choice = dataSourceChoices[i][0];
      if (value === choice) {
        humanReadableValue = dataSourceChoices[i][1];
        break;
      }
    }
    return humanReadableValue;
  };
  function updateChartDataFunc(chartData, savedData) {
    var categoryFound = false;
    // If an entry for this category exists in the chartData array, increment its counter
    for (var i = 0; i < chartData.length; i++) {
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
  var bins = this.bins.freeResponseIntercept[resultType];
  if (bins === undefined) {
    throw new Error('No bins found for type ' + resultType);
  }
  function initChartDataFunc() {
    var chartData = [];
    // Initialize the chart data with empty values for each bin
    bins.forEach(function(bin, idx, arr) {
      // The binning function places values into bins by checking if the value
      // is strictly less than the bin. Since bin === bin, make each bin a hair
      // smaller so that it passes the check
      var downStep = (idx === 0) ? bin / 2 : (bin - arr[idx - 1]) / 2;
      formattedBin = binValue(bin - downStep, arr);
      chartData.push([formattedBin, 0]);
    });
    // Add an extra bin value to make sure that the max gets displayed
    chartData.push([String(bins[bins.length - 1]) + '+', 0]);
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

ChartHelper.prototype.getSeriesName = function() {
  /**
   * Get the Highcharts series name for a given survey run.
   */
  if (this.surveys.length == 0) {
    throw new Error('At least one survey is required to generate a series name');
  }
  // Get the timestamps of the oldest and newest runs of this survey
  var minDate;
  var maxDate;
  for (var i = 0; i < this.surveys.length; i++) {
    var surveyStart = new Date(this.surveys[i]['time_start']);
    var surveyStop = new Date(this.surveys[i]['time_stop']);

    if (!minDate || surveyStart < minDate) {
      minDate = surveyStart;
    }
    if (!maxDate || surveyStop > maxDate) {
      maxDate = surveyStop;
    }
  }
  // Format a date range
  minDate = minDate.toLocaleDateString();
  maxDate = maxDate.toLocaleDateString();
  var dateRange = (minDate !== maxDate) ? minDate + ' - ' + maxDate : minDate;
  // Add the N for the surveys
  var numSurveysPrefix = ' (' + String(this.surveys.length);
  var numSurveysSuffix = (this.surveys.length > 1) ? ' surveys)' : ' survey)';
  var numSurveys = numSurveysPrefix + numSurveysSuffix;
  return dateRange + numSurveys;
}

ChartHelper.prototype.destroyChart = function(chartId) {
  /**
   * Destroy a Highcharts chart.
   * @param {String} chartId - The ID attribute of the chart container on the page.
   */
  var chart = $('#' + chartId).highcharts();
  chart.destroy();
}

ChartHelper.prototype.addAcsSeries = function(chartId, acsData, seriesName) {
  /**
   * Add a Higcharts series for an ACS data source to the chart.
   * @param {String} chartId - The ID attribute of the chart container on the page.
   * @param {Object} acsData - An object where the attributes are FIPS codes and the
   *                           values are objects representing ACS data for that FIPS code.
   * @param {String} seriesName - A string to use for the name of the series.
   */
  var chart = $('#' + chartId).highcharts();
  var seriesOpts = {
    id: 'acs-' + seriesName,
    name: seriesName,
    data: []
  };
  // Make sure that the order of the incoming ACS series matches the order of the
  // categories in the existing series
  var categories = chart.xAxis[0].categories;
  var formattedAcsData = [];
  for (var i = 0; i < categories.length; i++) {
    var category = categories[i];
    var recordedValue = (acsData.data[category]) ? acsData.data[category] : 0;
    formattedAcsData.push([category, recordedValue]);
  }
  // Format ACS data as percentiles
  var percentileData = percentiles(formattedAcsData);
  for (var i = 0; i < percentileData.length; i++) {
    seriesOpts.data.push(percentileData[i][1]);
  }
  chart.addSeries(seriesOpts, true, true);  // Force the chart to redraw
}

ChartHelper.prototype.removeAllAcsSeries = function(chartId) {
  /**
   * Remove all ACS data series from the chart.
   */
  var chart = $('#' + chartId).highcharts();
  // Since we'll be deleting series in the forthcoming loop, we need to stash the
  // length ahead of time.
  var numSeries = chart.series.length;
  for (var i = numSeries - 1; i > -1; i--) {
    if (chart.series[i].options.id && chart.series[i].options.id.startsWith('acs-')) {
      chart.series[i].remove(true); // 'true' forces the chart to redraw
    }
  }
}

function quintiles(categories) {
  /**
   * Given an array map of categories and numbers, return an array of quintiles
   * for each category in the array.
   * Algorithm adapted from:
   * https://github.com/compute-io/quantiles
   * @param {Array} categories - A nested set of arrays acting as a Map, where
   *                             the first element represents a category name and the
   *                             second element is an array of numbers representing
   *                             all recorded values for that category.
   */
  return categories.map(function(category) {
    var categoryName = category[0];
    var numArr = category[1].slice();
    if (numArr.length < 5) {
      throw new Error('Quintiles can only be computed for arrays of length >=5, got ' + String(numArr.length))
    }
    numArr.sort(function(a, b) { return a - b; });
    var quintiles = [];
    quintiles[0] = numArr[0];
    quintiles[5] = numArr[numArr.length - 1];
    for (var i = 1; i < 5; i++) {
      // Calculate the vector index marking the quantile
      id = (numArr.length * i / 5) - 1;
      // Is the index an integer?
      if (id === Math.floor(id)) {
        // Value is the average between the value at id and id+1:
        val = (numArr[id] + numArr[id + 1]) / 2.0;
      } else {
        // Round up to the next index:
        id = Math.ceil(id);
        val = numArr[id];
      }
      quintiles[i] = val;
    }
    return [categoryName, quintiles];
  });
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
    var numArr = category[1].slice();
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
  return categories.map(function(category) { return [category[0], Math.round((category[1] / total) * 100)] })
}

function binValue(value, bins) {
  /**
   * Bucket a value according to a set of bins.
   * @param {Number} value - The value to bin.
   * @param {Array} bins - The bins to use for bucketing. The function assumes
   *                       that these bins are sorted in ascending order.
   */
  var binnedValue;
  for (var i = 0; i < bins.length; i++) {
    var bin = bins[i];
    if (value < bin) {
      if (i === 0) {
        binnedValue = '0-' + String(bin-1);
        break;
      } else {
        var prevBin = bins[i - 1];
        // Check if the bin represents a single integer instead of a range
        if (prevBin === bin - 1) {
          binnedValue = String(bin);
        } else {
          binnedValue = String(prevBin) + '-' + String(bin - 1);
        }
        break;
      }
    }
  }
  if (binnedValue === undefined) {
    // Value was larger than all bins
    binnedValue = String(bins[bins.length - 1]) + '+';
  }
  return binnedValue;
}

/**
 * Shuffles array in place. ES6 version
 * @param {Array} a items An array containing the items.
 */
function shuffle(a) {
    for (var i = a.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [a[i], a[j]] = [a[j], a[i]];
    }
    return a;
}
