const { data } = require("jquery");

function getIQ(){
    let file = $('#dataFile').prop('files')[0];
    // File Checking
    // Check if it's the correct filetyp

    // Actual file processing    
    file.text().then(text => {
        let data = $.csv.toArrays(text);
        console.log(data);
    }).catch(err => {
        console.error(err);
    })
    return false;
    
    // Do some CSV voodoo magic here
}

function sendData(){
    console.log("Sent")
}

$(document).ready(function(){
    $("#submitFile").click(function(){
        sendData();
    })
})