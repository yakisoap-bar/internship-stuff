const ctx = document.getElementById('myChart');

let deco = {
    bgCol: ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'],
    borderCol: [ 'rgba(255, 99, 132, 1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)']
}

let records = {
    labels: ['Wifi', 'BNET', 'FASTNET', 'Bluetooth', '4G', 'FM'],
    data: [12, 19, 3, 5, 2, 3]
}

let chartData = {
    type: 'bar',
    data: {
        labels: records.labels,
        datasets: [{
            label: 'No. of records',
            data: records.data,
            backgroundColor: deco.bgCol,
            borderColor: deco.borderCol,
            borderWidth: 1
        }]
    },
    options: {
        indexAxis: 'y',
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
};

const myChart = new Chart(ctx, chartData);

/*
let test = {
    num: 4-1
}

print(test)
*/