function filterData(){
    let fileData = $('#fileData');
    console.log(fileData);
}

function sendData(){
    console.log("Sent")
}

$(document).ready(function(){
    $("#submitFile").click(function(){
        filterData();
        sendData();
    })
})