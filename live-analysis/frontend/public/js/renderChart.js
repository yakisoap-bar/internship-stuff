
function getData(recv){
   // Data shld alr be sorted
   let results = {
       "labels": recv[1],
       "data": recv[0],
   }

   // Turn into float
   results.data = convertToFloat(results.data);

   return results;
}

function convertToFloat(data){
   for(let i=0; i<data.length; i++){
       data[i] = parseFloat(data[i]);
   };
   return data;
}

let results = getData([[19, 12, 5, 3, 3, 2], ['BNET', 'Wifi', 'FASTNET', 'Bluetooth', 'FM', '4G']]);

function chartData(results){
    // Need to find a way to generate the colours better
    let deco = {
        bgCol: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'],
        borderCol: [ 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'],
        borderWidth: 1,
    };

    // Determining the type of bar chart
    let options = {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    };

    // Data
    let records = {
        labels: results.labels,
        datasets:[{
            label: 'No. of records',
            data: results.data,
            backgroundColor: deco.bgCol,
            borderColor: deco.borderCol,
            borderWidth: deco.borderWidth
        }]
    };

    // Final one that goes in
    let chartData = {
        type: 'bar',
        data: records,
        options: options
    };

    return chartData;
};