// retrieve container element from `trend_chart.html` to plot bar chart for hotel booking
var ctx = document.getElementById('barChart').getContext('2d');


$(document).ready(function () {
    $('#username').change(function () {
        var username = $('#username').val();
        $.ajax({
            url: '/dashboard_due_per_user',
            type: 'POST',
            data: {
                username: username
            },
            success: function (data) {

                // retrieve hotel booking income data (chart dimension) and x-axis labels (chart labels).
                var xLabels = data.chartDim;
                var yLabels = data.userChartLabel;
                var user_due = data.user_name;

                console.log(xLabels)
                console.log(yLabels)

                // clear the chart to get new data coming as we click on the select dropdown
                let chartStatus = Chart.getChart("barChart")
                if (chartStatus) {
                    chartStatus.destroy()
                }

                // with the existing container element, create a bar chart to display income data
                var barChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: xLabels,
                        datasets: [
                            {
                                label: `Booking Due Per User By ${user_due}`,
                                data: yLabels,
                                backgroundColor: "#c9a946"
                            }
                        ]
                    }
                });
            }
        });
    });
});
