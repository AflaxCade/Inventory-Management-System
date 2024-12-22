// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

// Bar Chart Example
var ctx = document.getElementById("myBarChart");
var myBarChart = new Chart(ctx, {
  type: 'bar',
  data: {
    labels: barLabels, // Use product names as labels
    datasets: [{
      label: "Total Sold",
      backgroundColor: "#4e73df", // Primary color for the bars
      hoverBackgroundColor: "#2e59d9", // Hover color for the bars
      borderColor: "#4e73df", // Border color
      data: barData, // Use total quantities sold as data
    }],
  },
  options: {
    maintainAspectRatio: false,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },
    scales: {
      xAxes: [{
        time: {
          unit: 'product' // Unit as 'product' for product names
        },
        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 5 // Limit to top 5 products
        },
        maxBarThickness: 25, // Maximum bar thickness
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: Math.max(...barData), // Dynamically adjust the Y-axis max value + 10
          maxTicksLimit: 5,
          padding: 10,
          // Add "units" to Y-axis labels
          callback: function(value, index, values) {
            return value + ' units'; // Display as "X units"
          }
        },
        gridLines: {
          color: "rgb(234, 236, 244)", // Grid line color
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false // Hide legend
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)", // Tooltip background
      bodyFontColor: "#858796", // Tooltip text color
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + ': ' + tooltipItem.yLabel + ' units'; // Tooltip format
        }
      }
    },
  }
});