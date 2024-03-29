let ctx = document.getElementById('myChart');

function formatData(recv){
    // Data shld alr be sorted
    // This was a misconception, mission abort
    let predictions = recv.data.predictions;
    let signalNames = recv.data.signalNames;
    let lenNum = signalNames.length;

   // Sort
   let temp = []
   for(let i=0; i<lenNum; i++){
       temp[i] = [convertToFloat(predictions[i]), signalNames[i]] 
   }

   temp.sort()
   temp.reverse()

    let formattedData = {
       "data": [],
       "labels": []
   }

   for (i=0; i<lenNum; i++){
       formattedData.data[i] = temp[i][0];
       formattedData.labels[i] = temp[i][1];
   }


   return formattedData;
}

function convertToFloat(data){
   for(let i=0; i<data.length; i++){
       data[i] = parseFloat(data[i]);
   };
   return data;
}

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
            },
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