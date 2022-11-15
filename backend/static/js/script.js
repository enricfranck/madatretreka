$(document).ready(function(){
    $("#circuit-details div").hide();
    $("p").click(function(){
        $(this).next("div").slideToggle("fast").siblings("div:visible").slideUp("fast");
    })
})