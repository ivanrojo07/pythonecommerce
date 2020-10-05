
function renderChart(id, data, labels){
    var ctx = $("#"+id)
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: "Sales",
                data: data,
                backgroundColor:  "rgba(0, 158, 29, 0.45)",
                borderColor: "rgba(0, 158, 29, 1)"
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            }
        }
    });
}

function getSalesData(type,id){
    var url = "/analytics/sales/data/"
    var method = "GET"
    var data = {
        "type" : type
    }
    $.ajax({
        url: url,
        method: method,
        data: data,
        success: function(responseData){
            console.log(responseData)
            renderChart(id,responseData.data, responseData.labels)
        },
        error: function(error){
            $.alert("An error occurred")
        }
    })
}

//getSalesData("week","thisWeekSales")
//getSalesData("4weeks","fourWeekSales")
var chartsToRender = $(".render-chart")
$.each(chartsToRender, function(index, html){
   var $this = $(this)
   if ($this.attr('data-type') && $this.attr('id')){
        getSalesData($this.attr('data-type'), $this.attr('id'))
   }
})
