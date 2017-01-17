
function uploadSize() {
    if (typeof ($('#photo_fn')[0].files) != "undefined") {
        //check upload file size
        var size = parseFloat($('#photo_fn')[0].files[0].size / 1024 / 1024).toFixed(2); // cal the file size in MB
        if (size > 10) {
            $('#photo-msg').text('Maximum upload file size is 10MB!');
            return false;
        }

        //check the upload file format/exteions
        var type = $('#photo_fn')[0].files[0].type;
        console.log(type);
        if (type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" || type == "application/vnd.ms-excel") {
            return true;
        }
        else {
            $('#photo-msg').text('Not a valid MS excel file, only allow for ".xls", ".xlsx"!');
            return false;
        }
    }
}
function getFilePath() {
    var fullPath = document.getElementById("#photo_fn").value;
    fileName = fullPath.split(/(\\|\/)/g).pop();
    document.getElementById("photo_name").value = fileName;
}