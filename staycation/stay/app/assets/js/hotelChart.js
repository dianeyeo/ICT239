// retrieve container element from `trend_chart.html` to plot bar chart for hotel booking
var ctx = document.getElementById('barChart').getContext('2d');


$(document).ready(function () {
    $('#hotel_due').change(function () {
        var hotelname = $('#hotel_due').val();
        $.ajax({
            url: '/dashboard_due_per_hotel',
            type: 'POST',
            data: {
                hotel_due: hotelname
            },
            success: function (data) {

                // retrieve hotel booking income data (chart dimension) and x-axis labels (chart labels).
                var xLabels = data.chartDim;
                var yLabels = data.hotelChartLabel;
                var due_hotel = data.user_name;

                console.log(xLabels)
                console.log(yLabels)

                // clear the chart to get new data coming as we click on the select dropdown
                let chartStatus = Chart.getChart("barChart")
                if (chartStatus) {
                    chartStatus.destroy()
                }

                // with the existing conatiner element, create a bar chart to display income data
                var barChart = new Chart(ctx, {
                    type: "bar",
                    data: {
                        labels: xLabels,
                        datasets: [
                            {
                                label: `Booking Due Per Hotel By ${hotelname}`,
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