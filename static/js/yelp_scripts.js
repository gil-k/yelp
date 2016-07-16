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


var default_term;
var default_loc;
var map;
var markers = [];
var mapOptions = {
    zoom: 11,
    // center: new google.maps.LatLng(32.77, -122),
    mapTypeId: google.maps.MapTypeId.ROADMAP
};

function initGil(){
    alert("Feel Confident, Gil!");
};
function set_defaults(term, loc){
    default_term = term;
    default_loc = loc; 
}
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

function searchYelp(){ 
    initInputFields();

    var $loading_overlay = $("#loading_overlay"),
        $spinner = $("#spinner"),
        $spinner_background = $("#spinner_background");

    var term = document.getElementById('term').value;
    var location = document.getElementById('location').value;
    term = term.trim();
    location = location.trim();

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
            status = data['status'];
            if(status == 'ok'){
                coords = data['coords'];
                lats = data['lats'];
                lngs = data['lngs'];
                initMap(coords, lats, lngs);
            };

            $("#search_results").html(data['html']);

            $loading_overlay.hide();
            $spinner.hide();
            $spinner_background.hide();
        },
        error: function( data ) {
            $loading_overlay.hide();
            $spinner.hide();
            $spinner_background.hide();
            response = json.loads(data);
            alert('Oops! Something went wrong.  Please retry.');
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
