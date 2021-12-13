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

    csvRaw.text().then(text => {;
        let data = processFile(text);

        axios.post(URL, {
            "data": data
        },
        {
            "headers": { 
                'Content-Type': 'application/json'
        }
    }).then(function(results){
            const myChart = new Chart(ctx, chartData(results));
        }).catch(error => {
            console.log(error);
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

    // turn into nice array
    // [[I,Q],[I,Q]...]
    data = data.split('\n')
    for(let i=0; i<data.length; i++){
        data[i] = data[i].split(',');
        
        // Convert to floats
        data[i][0] = parseFloat(data[i][0])
        data[i][1] = parseFloat(data[i][1])

        if (Number.isNaN(data[i][0]) || Number.isNaN(data[i][0])){
            data.splice(i, 1);
            i--;
        } else{
            data[i] = [[data[i][0]*1024], [data[i][1]*1024]];
        };
    }

    return data;
}
