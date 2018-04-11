$(document).ready(function(){

    $("#google-search-button").click(function(event){
        event.preventDefault();

        var question = $("#question").val();
        var win = window.open("https://www.google.com/search?q=define " + question);
        if (win) {
            win.focus();
        } else {
            alert("Please, allow popups for this website.");
        }

    });

});