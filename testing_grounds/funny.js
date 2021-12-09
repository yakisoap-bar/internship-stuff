$(() => {
    $('#dataSubmit').on('click', () => {
        var data = $('#dataFile').prop('files')[0];
        data.text().then(text => {
            var temp = $.csv.toArrays(text);
            console.log(temp);
        }).catch(err => {
            console.error(err);
        })

        return false;
    })
})