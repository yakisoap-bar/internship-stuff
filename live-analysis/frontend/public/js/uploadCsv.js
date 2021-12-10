const { data } = require("jquery");

function sendData(){
    // File handling
    let data = $('#dataFile').prop('files')[0];
    let check = "";

    // Check filetype
    check = checkFile(data);
    if (check != ""){
        console.error(check);
        return false;
    }

    data.text().then(text => {
        // Process into to IQ data
        processFile(data);
    }).catch(err => {
        console.error(err);
    })

    return false;
}

function checkFile(file){
    let check = "";
    let errMsg = "Invalid file!"
    try{
        let name = file.name;
        name = name.split('.')[1];
    } catch{
       return errMsg
    }
    if (file.type != "application/vnd.ms-excel"){
        check = errMsg;
    } else if(file.type != "text/plain" && name != "csv"){
        check = errMsg;
    }

    return check;
}

function processFile(data){
    //turn into a nice array
    console.log("processFile")
};