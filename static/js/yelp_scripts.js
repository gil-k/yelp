$(document).ready(function() {
    var $window = $(window),
        $mapEl = $("#map"),
        $bannerEl = $('#top_banner');
        // $stickyBussInfo = $('#buss_info'),
        // elTop = $mapEl.offset().top;
    $window.scroll(function() {
      // $mapEl.toggleClass('stickTop', $window.scrollTop() > elTop);
      $mapEl.css({right: '0px', position: 'fixed'});
      $bannerEl.toggleClass('stickTop', true);
      //$stickyBussInfo.toggleClass('sticky', true);
    });


    $("#term").keyup(function (e) {
        if (e.keyCode == 13) {
            searchYelp();
        }
    });
    $("#location").keyup(function (e) {
        if (e.keyCode == 13) {
            searchYelp();
        }
    });


    $(document).on('mouseenter', '#buss_container', function(e) {
        var index = $('#search_results #buss_container').index(this);
        markers[index].setLabel( { text: (index+1).toString() , color: 'black', fontWeight : 'bold' ,} ) ;
        markers[index].setZIndex(google.maps.Marker.MAX_ZINDEX + 1);
    });

    // 
    $(document).on('mouseleave', '#buss_container', function(e) {
        var index = $('#search_results #buss_container').index(this);
        markers[index].setLabel( { text: (index+1).toString() , color: 'white'} ) ;
        markers[index].setZIndex(google.maps.Marker.MAX_ZINDEX);
    });
});

function initGil(){
    alert("Feel Confident, Gil!");
};


var map;
var markers = [];
var mapOptions = {
    zoom: 11,
    center: new google.maps.LatLng(32.77, -122),
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

function initMap0() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.785, lng: -122.4040},
        zoomControl: true,
        mapTypeControl: false,
        scaleControl: false,
        streetViewControl: false,
        rotateControl: false,
        fullscreenControl: false,
        zoom: 11
    });
    // map = new google.maps.Map(document.getElementById('map'), mapOptions);
    // for (var i=0; i<markerData.length; i++) {
    //     markers.push(
    //         new google.maps.Marker({
    //             position: new google.maps.LatLng(markerData[i].lat, markerData[i].lng),
    //             // title: markerData[i].title,
    //             map: map,
    //             // icon: normalIcon()
    //         })
    //     );
    // }
};

 
// function highlightMarker() {
//   return {
//     // url: 'http://steeplemedia.com/images/markers/markerGreen.png'
//   };
// }

function initMap(coords, lats, lngs, rank) {
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

    // var marker;
    // for (var i=0; i < (coords); i++){ 
    //     marker = new google.maps.Marker({
    //         position: {lat: lats[i], lng: lngs[i]},
    //         label: {
    //                 text: (i+1).toString(), 
    //                 color: 'white'
    //                 },
    //         title: '',
    //         icon: '',
    //         map: map
    //     })      
    // };

    // var marker;
    // if(rank == null){
    //     for (var i=0; i < (coords); i++){ 
    //         marker = new google.maps.Marker({
    //             position: {lat: lats[i], lng: lngs[i]},
    //             label: {
    //                     text: (i+1).toString(), 
    //                     color: 'white'
    //                     },
    //             map: map
    //         });        
    //     };
    // } else {
    //     var hovered_buss = parseInt(rank); 
    //     for (var i=0; i < (coords); i++){ 
    //         if(hovered_buss != i){
    //             marker = new google.maps.Marker({
    //                 position: {lat: lats[i], lng: lngs[i]},
    //                 label: {
    //                         text: (i+1).toString(), 
    //                         color: 'white'
    //                         },
    //                 map: map
    //             });
    //         } else {
    //             // alert(hovered_buss);
    //         }
    //     };
            
    //     marker = new google.maps.Marker({
    //         position: {lat: lats[hovered_buss], lng: lngs[hovered_buss]},
    //         label: {
    //                 text: (i+1).toString(), 
    //                 color: 'black'
    //                 },
    //         zIndex: google.maps.Marker.MAX_ZINDEX + 1,
    //         map: map
    //     });            
    // }
};  

function searchYelp(){ 
    var $loading_overlay = $("#loading_overlay"),
        $spinner = $("#spinner"),
        $spinner_background = $("#spinner_background");

    var term = document.getElementById('term').value;
    var location = document.getElementById('location').value;
    var url = "/search/?term=" + term + "&location=" + location;

    window.scrollTo(0, 0);

    $loading_overlay.show();
    $spinner.show();
    $spinner_background.show();

    // $("#spinner_background").style.display = 'inline-block'; 

    $.ajax({
        url: url,
        dataType: 'json',
        success: function( data ) {
            coords = data['coords'];
            lats = data['lats'];
            lngs = data['lngs'];

            $("#search_results").html(data['html']);

            initMap(coords, lats, lngs);
            // initMap();

            // $("#spinner_background").style.display = 'none'; 
            $loading_overlay.hide();
            $spinner.hide();
            $spinner_background.hide();
        },
        error: function( data ) {
            $loading_overlay.hide();
            $spinner.hide();
            $spinner_background.hide();
            // print "yelp exception"
            // print data
            text = 'Oops!  There was a problem accessing data from Yelp.  Please verify your inputs and retry.'
            alert(text);
        }
    });

    // $.getJSON(url, function(data){
    //     // $("#search_results").html(data);
    //     coords = data['coords'];
    //     lats = data['lats'];
    //     lngs = data['lngs'];

        

    //     $("#search_results").html(data['html']);

    //     initMap(coords, lats, lngs);

    //     // $("#spinner_background").style.display = 'none'; 
    //     $loading_overlay.hide();
    //     $spinner.hide();
    //     $spinner_background.hide();
    //   });
};
