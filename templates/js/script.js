d3.json('./info.json', function(error, data){
    console.log(data);
    var ctx = document.getElementById('loss_chart').getContext('2d');
    var labels = [];
    var y = [];
    var i;
    for(i=0;i < data.length;++i){
        labels.push(i.toString());
        y.push(data[i].loss);
    }
    var chart = new Chart(ctx, {
        // The type of chart we want to create
        type: 'line',


        // The data for our dataset
        data: {
            labels: labels, 
            datasets: [{
                label: "Loss",
                borderColor: 'rgb(255, 99, 132)',
                data: y,
            }]
        },

        // Configuration options go here
        options: {}
    });
});
