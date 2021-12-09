const ctx = document.getElementById('myChart');

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
    labels: 'No. of records',
    datasets:[{
        label: ['Wifi', 'BNET', 'FASTNET', 'Bluetooth', '4G', 'FM'],
        data: [12, 19, 3, 5, 2, 3],
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

const myChart = new Chart(ctx, chartData);