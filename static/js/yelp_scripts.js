$(document).ready(function() {
    // keeps banner at the top, and google map at top-right
    var $window = $(window),
        $mapEl = $("#map"),
        $bannerEl = $('#top_banner');
    $window.scroll(function() {
      $mapEl.css({right: '0px', position: 'fixed'});
      $bannerEl.toggleClass('stickTop', true);
    });

    // after entry in term/category search input field, pressing ENTER starts Yelp search
    $("#term").keyup(function (e) {
        if (e.keyCode == 13) {
            searchYelp();
        }
    });
    // after entry in location search input field, pressing ENTER starts Yelp search
    $("#location").keyup(function (e) {
        if (e.keyCode == 13) {
            searchYelp();
        }
    });

    // mouse hovering over biz-photos highlights corresponding google map marker
    $(document).on('mouseenter', '#buss_container', function(e) {
        var index = $('#search_results #buss_container').index(this); 
        markers[index].setLabel( { text: (index+1).toString() , color: 'black', fontWeight : 'bold' ,} ) ;
        markers[index].setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
    });

    // mouse leaving a row of biz-photos returns the corresponding google map marker to normal state
    $(document).on('mouseleave', '#buss_container', function(e) {
        var index = $('#search_results #buss_container').index(this);
        markers[index].setLabel( { text: (index+1).toString() , color: 'white'} ) ;
        markers[index].setZIndex(google.maps.Marker.MAX_ZINDEX);
    });
});

// default term/category query string for Yelp API
var default_term;
// default location query string for Yelp API
var default_loc;
// Google map with markers of businesses displayed on page
var map;
// list of Google map markers for businesses displayed on page
var markers = [];

// default term/category & location Yelp API query strings for search
function set_defaults(term, loc){
    default_term = term;
    default_loc = loc; 
}

// location map with business markers
function initMap(coords, lats, lngs, rank) {
    markers = [];
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: lats[coords], lng: lngs[coords]},
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        zoom: 11
    });

    // keep markers in an array, so they can be retrieved later for highlighting
    for (var i=0; i<coords; i++) {
        markers.push(
          new google.maps.Marker({
            position: new google.maps.LatLng(lats[i], lngs[i]),
            label: {
                    text: (i+1).toString(), 
                    color: 'white'
                    },
            map: map
          })
        );
    }
};  

// if input field is empty, populate with default values
function initInputFields(){ 
    $el_term = document.getElementById('term');
    if($el_term.value.trim() === ''){
        $el_term.value = default_term;
    }
    $el_loc = document.getElementById('location');
    if($el_loc.value.trim() === ''){
        $el_loc.value = default_loc;
    }
};

// animation while waiting for response and display of biz-photos
function loading_anim(bool){
    var $loading_overlay = $("#loading_overlay"),
        $spinner = $("#spinner"),
        $spinner_background = $("#spinner_background");

    if (bool){
        $loading_overlay.show();
        $spinner.show();
        $spinner_background.show();
    } else {
        $loading_overlay.hide();
        $spinner.hide();
        $spinner_background.hide();       
    }
}

// do Yelp search and display biz-photos of businesses
function searchYelp(){ 
    // if input field is empty, populate with default values
    initInputFields();

    // loading animation
    var $loading_overlay = $("#loading_overlay");
    var $spinner = $("#spinner");
    var $spinner_background = $("#spinner_background");

    // term/category and region/location information to search
    var term = document.getElementById('term').value;
    var location = document.getElementById('location').value;
    term = term.trim();
    location = location.trim();

    // construct the search and location term, append to url
    var url = "/search/?term=" + term + "&location=" + location;

    window.scrollTo(0, 0);

    // animation during request & processing of query response
    loading_anim(true);

    // 'search' endpoint for Yelp search API
    $.ajax({
        url: url,
        dataType: 'json',
        success: function( data ) {
            status = data['status'];
            if(status == 'ok'){
                coords = data['coords'];
                lats = data['lats'];
                lngs = data['lngs'];
                initMap(coords, lats, lngs);
            };

            // displays business info & biz-photos per row within search_results div
            $("#search_results").html(data['html']);

            // stop animation
            loading_anim(false);
        },
        error: function( data ) {
            // stop animation
            loading_anim(false);
            alert('Oops! Something went wrong.  Please retry.');
        }
    });        
};
