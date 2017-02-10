$("#file_fn").change(function(){
    getFilePath('file_fn', 'file_name', 'id_name');
})

$('form').submit(function(){
    return uploadSize('#file_fn', '#file_msg');
})