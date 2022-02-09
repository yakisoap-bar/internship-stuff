const URL = 'http://localhost:3000/predict';

function sendData(){
    // File handling
    let csvRaw = $('#dataFile').prop('files')[0];
    let check = "";

    // Check filetype
    check = checkFile(csvRaw);
    if (check != ""){
        console.error(check);
        return false;
    }

    $(`#status`).html(`<p id="status">Uploading...</p>`);

    csvRaw.text().then(text => {;
        let toProcess = processFile(text);
        toProcess = toProcess[0]

        axios.post(URL, {
            "data": toProcess,
            "frequency": 4000
        }
        ).then(function(results){
            console.log("done")
            $(`#status`).html(`<p id="status">Done!</p>`);
            let formattedChartData = formatData(results)
            const myChart = new Chart(ctx, chartData(formattedChartData));
        }).catch(error => {
            $(`#status`).html(`<p id="status">Error!</p>`);
            console.error(error);
        })
    })

    return false;
}

function checkFile(file){
    let check = "";
    let errMsg = "Invalid file!"
    let name = file.name;
    try{
        name = name.split('.')[1];
    } catch(e){
       return e;
    }
    if (file.type != "application/vnd.ms-excel"){
        check = errMsg;
    } else if(file.type != "text/plain" && name != "csv"){
        check = errMsg;
    }

    return check;
}

function processFile(file){
    let data = file;

    // Sort out nums
    data = data.split('\n')
    for(let i=0; i<data.length; i++){
        data[i] = data[i].split(',');
        
        // Convert to floats
        data[i][0] = parseFloat(data[i][0])
        data[i][1] = parseFloat(data[i][1])

        if (Number.isNaN(data[i][0]) || Number.isNaN(data[i][0])){
            data.splice(i, 1);
            i--;
        }
    }

    // turn into nice array
    // [[I,Q],[I,Q]...]
    data = math.transpose(data);
    if (data[0].length >= 1024){
        i=1
        let parsedData = [];
        while (i*1024 <= data[0].length){
            parsedData[i-1] = [data[0].slice(i-1, i*1024), data[1].slice(i-1, i*1024)];
            i++;
        }
        data = [parsedData];
    }
    return data;
}
