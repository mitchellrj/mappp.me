/*jslint nomen: true, unparam: true, white: true, browser: true */
/* global jQuery: true, google: true */
(function($) {
	"use strict";
	
	window.mappp = window.mappp || {};
	var M = window.mappp.me = window.mappp.me || {};
	
    M.static_url = $('script[src$="mappp.me.gmap.js"]').attr('src').replace('js/mappp.me.gmap.js', '');
	
	M.gmap = {
	  updateLocation: function (lat, lng) {
	    var position = new google.maps.LatLng(lat, lng),
	        markerImage = {
	    		url: M.static_url +
	    		     'images/pointer-small-filled-transparent.png'
	    	},
	        params = {
		        icon: markerImage,
		        flat: true,
		        clickable: false,
		        map: M.gmap._map,
		        position: position
		    };
	    M.gmap._map.setCenter(position);
	    if (M.gmap._marker) {
	      M.gmap._marker.setMap(null);
	    }
	    M.gmap._marker = new google.maps.Marker(params);
	  }
	};
	
	$(function() {
	  var lat = M.initial.latitude,
	      lng = M.initial.longitude,
	      zoom = M.initial.zoom,
	      params = {
		      mapType: google.maps.MapTypeId.ROADMAP,
		      zoom: zoom,
		      center: new google.maps.LatLng(lat, lng),
		      mapTypeControl: true,
		      zoomControl: true,
		      panControl: true
	      };
	  M.gmap._map = new google.maps.Map(document.getElementById("map"),
	                                           params);
	  google.maps.event.addListener(M.gmap._map, 'zoom_changed',
	       function() {
	         var newZoom = M.gmap._map.getZoom(),
	             currentGmapLink = $('#gmap-link').attr('href'),
	             newGmapLink = currentGmapLink.replace(
	                 /(\?|&)z=(\d+)($|&)/i,
	                 function(match, delimiter) {
	                	 return delimiter + 'z=' + (newZoom) + '&';
	                 });
	         document.cookie='zoom='+newZoom;
	         $('#gmap-link').attr('href', newGmapLink);
	       });
	  M.gmap.updateLocation(lat, lng);
	});
}(jQuery));