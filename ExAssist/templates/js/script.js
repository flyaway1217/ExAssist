d3.json('./info.json', function(error, data){
    window.data = data;
    printValues(data);
});

function colortList(){
    reval = [];
    reval.push('rgb(255,  0, 0)');
    reval.push('rgb(0,  255, 0)');
    reval.push('rgb(0,  0, 255)');
    reval.push('rgb(255,  0, 255)');
    reval.push('rgb(255,  255, 0)');
    return reval;
}


function update(choices, min, max){
    data = window.data;
    var i;
    labels = [];
    plot_data = [];
    for(i=min;i < max;++i){
        labels.push(i.toString());
    }
    choices.forEach(function(name){
        tmp_data = [];
        for(i=min; i < max;++i){
            tmp_data.push(data[i][name]);
        }
        plot_data.push(tmp_data);
    });

    objects = [];
    colors = colortList();
    choices.forEach(function(name, i){
        obj = {
            label: name, 
            borderColor: colors[i%5],
            data: plot_data[i],
        };
        objects.push(obj);
    });

    var ctx = document.getElementById('chart').getContext('2d');
    if (window.fig != undefined){
        window.fig.destroy();
    }
    window.fig = new Chart(ctx, {
        type: 'line', 
        data:{
            labels: labels, 
            datasets: objects, 
        }, 
        options:{}
    });
}

function chooseData(){
    data = window.data;

    var choices = [];
    d3.selectAll('.box').each(function(d){
        cb = d3.select(this);
        if (cb.property('checked')){
            choices.push(cb.property('value'));
        }
    });
    
    var min = parseInt(d3.select('#start').property('value'));
    var max = parseInt(d3.select('#end').property('value'));

    if (min < 0 || min > max || max > data.length || max < 0){
        return;
    }

    if(choices.length > 0){
        update(choices, min, max);
    }
} 
function printValues(data){
    var values = [];
    for (var name in data[0]){
        values.push(name);
    }
    d3.select('#value').selectAll('input')
        .data(values)
        .enter()
        .append('span')
            .attr('class', 'boxlabel')
        .append('input')
            .attr('class', 'box')
            .attr('type', 'checkbox')
            .property('checked', function(d){
                if(d == 'loss'){
                    return true;
                }
                else{
                    return false;
                }
            })
            .attr('onClick', 'chooseData()')
            .attr('value', function(d, i){
                return d;
            });
    d3.selectAll('.boxlabel')
        .style('display', 'inline-block')
        .style('width', '80px')
        .append('text')
        .text(function(d){return d;});

    d3.select('#start').attr('value', 0);
    d3.select('#end').attr('value', data.length);
    chooseData();
}
