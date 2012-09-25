window.mappp = window.mappp || {};
window.mappp.me = window.mappp.me || {};

window.mappp.me.gmap = {
  updateLocation: function (lat, lng) {
    var position = new google.maps.LatLng(lat, lng);
    mappp.me.gmap._map.setCenter(position);
    var markerImage = {
        url: mappp.me.static_url+'images/pointer-small-filled-transparent.png'
    };
    var params = {
        icon: markerImage,
        flat: true,
        clickable: false,
        map: mappp.me.gmap._map,
        position: position
    };
    if (mappp.me.gmap._marker) {
      mappp.me.gmap._marker.setMap(null);
    }
    mappp.me.gmap._marker = new google.maps.Marker(params);
  }
};

$(function() {
  mappp.me.static_url = $('script[src$="mappp.me.gmap.js"]').attr('src').replace('js/mappp.me.gmap.js', '');
  var lat = mappp.me.initial.latitude,
      lng = mappp.me.initial.longitude,
      zoom = mappp.me.initial.zoom;
  var params = {
      mapType: google.maps.MapTypeId.ROADMAP,
      zoom: zoom,
      center: new google.maps.LatLng(lat, lng),
      mapTypeControl: true,
      zoomControl: true,
      panControl: true
      };
  mappp.me.gmap._map = new google.maps.Map(document.getElementById("map"),
                                           params);
  google.maps.event.addListener(mappp.me.gmap._map, 'zoom_changed',
       function() {
         var newZoom = mappp.me.gmap._map.getZoom();
         document.cookie='zoom='+newZoom;
         $('#gmap-link').attr('href',
             $('#gmap-link').attr('href').replace(
                 /(\?|&)z=(\d+)($|&)/i,
                 function(match, delimiter) { return delimiter + 'z=' + (newZoom) + '&'; }
                 )
             );
       });
  mappp.me.gmap.updateLocation(lat, lng);
});