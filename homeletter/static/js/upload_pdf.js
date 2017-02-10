function uploadSize(name_id, msg_id) {
    if (typeof ($(name_id)[0].files) != "undefined") {
        //check upload file size
        var size = parseFloat($(name_id)[0].files[0].size / 1024 / 1024).toFixed(2); // cal the file size in MB
        if (size > 10) {
            $(msg_id).text('Maximum upload file size is 10MB!');
            return false;
        }

        //check the upload file format/exteions
        var type = $(name_id)[0].files[0].type;
        console.log(type);
        if (type == "application/pdf") {
            return true;
        }
        else {
            $(msg_id).text('Unsupported File! Only allow for ".pdf"!');
            return false;
        }
    }
    return true;
}

function getFilePath(pathname, filename, id_name) {
    var fullPath = document.getElementById(pathname).value;
    fileName = fullPath.split(/(\\|\/)/g).pop();
    document.getElementById(filename).value = fileName;
    document.getElementById(id_name).value = fileName.split('.')[0];
}