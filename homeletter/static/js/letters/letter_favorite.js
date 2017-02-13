$(document).ready(function(){
    $('.favorite').each(function(){
        $(this).click(function(){
            var pk = +$(this).next().text();
            var fav = +$(this).prev().text();
            if(fav >=0 && fav <5 ){
                fav++;
            }
            else if(fav == 5){
                fav = 0;
            }
            else{
                fav = fav;
            }
            $(this).prev().text(fav);

             starts = $(this).find('.star');
             for(i = 0; i < fav; i++){
                $(starts[i]).removeClass("fa-star-o").addClass("fa-star text-yellow");
             }
             for(i=5; i >= fav; i--){
                $(starts[i]).addClass("fa-star-o").removeClass("fa-star text-yellow");
             }

             //make ajax call
             $.ajax({
                url: '/letter/favorite/',
                type: 'get',
                data: {'favorite': JSON.stringify({'fav':fav, 'pk': pk})},
                success: function(data){
                    console.log(data);
                },
                error: function(){
                    console.log("SET FAVORITE FAILED!");
                }
             })
        });
    })
});

