$(function(){
    /*
        Initialize SlidesJS
    */
    $("#slides").slides({
        width: 375, /* WIDTH */
        height: 375, /* HEIGHT */
        effects: {
            navigation: "fade",
            pagination: "fade"
        },
        playInterval: 1500,
        fade: {
            interval: 1000,
            crossfade: true
        },
        startAtSlide: 0,
        /*
        navigateEnd: function( current ) {
            currentSlide( current );
        }, */
        loaded: function(){
            currentSlide( 1 );
        }
    });
    
    /*
        Play/stop button
    */
    $(".controls").click(function(e) {
        e.preventDefault();
        
        // Example status method usage
        var slidesStatus = $("#slides").slides("status","state");
        
        if (!slidesStatus || slidesStatus === "stopped") {

            // Example play method usage
            $("#slides").slides("play");

            // Change text
            $(this).text("Stop");
        } else {
            
            // Example stop method usage
            $("#slides").slides("stop");
            
            // Change text
            $(this).text("Play");
        }
    });
});
