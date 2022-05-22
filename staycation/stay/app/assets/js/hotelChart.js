// retrieve canvas element from `trend_chart.html` to plot trend chart for hotel booking income.
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
                var yLabels = data.chartXLabels;
                var due_hotel = data.user_name;

                console.log(xLabels)
                console.log(yLabels)

                // clear the chart to get new data coming as we click on the select dropdown
                let chartStatus = Chart.getChart("barChart")
                if (chartStatus) {
                    chartStatus.destroy()
                }

                // if dropdown is 'Select One', show empty chart
                // only when dropdown selects a user, then plot chart
                if (due_hotel != "Select One") {
                    // given existing canvas element, create a trend chart for display of income data
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
                        },
                        options: {
                            responsive: true,
                            maintainaspectratio: false,
                            scales: {
                                y: {
                                    ticks: {
                                        beginAtZero: true,
                                    }
                                },
                                x: {
                                    ticks: {
                                        autoSkip: true,
                                        padding: 10,
                                    }
                                }
                            }
                        }
                    });
                }
                else {
                    ctx.font = "20px Montserrat";
                    ctx.textAlign = "center";
                    ctx.fillText("Please Select an Option!", ctx.canvas.width / 2, ctx.canvas.height / 2);
                }
            }
        });
    });
});