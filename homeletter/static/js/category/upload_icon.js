$("#icon_fn").change(function(){
    getFilePath('icon_fn', 'icon_name');
})

$('form').submit(function(){
    return uploadSize('#icon_fn', '#icon_msg');
})