/*jslint nomen: true, regexp: true, unparam: true, white: true, browser: true */
/*global google: true, jQuery: true */
(function($) {
	"use strict";
	
	window.mappp = window.mappp || {};
	var M = window.mappp.me = window.mappp.me || {},
	    zoomRE = /(\?|&)(z(?:oom)?)=(\d+)($|&)/i;
	
	M.gmap = {
	    switchImage: function(uri) {
	      var map = $('#map img');
	      /* There is a memory leak in WebKit if we just replace the src.
	       * Replace the whole element instead.
	       */
	      map.replaceWith(
	          $('<div/>').append(
	              map.clone()
	                 .attr('src', uri)
	              ).remove()
	               .html()
	          );
	    },
	    updateLocation: function (lat, lng) {
		    var map = $('#map img'),
		        currentImageSrc = map.attr('src'),
		        newImageSrc = (currentImageSrc
		        	.replace(
		        	    // set the center to the new location
			        	/(\?|&)center=[0-9\.\-]+,[0-9\.\-]+(&|$)/i,
				        function(match, delimiter) {
				          return delimiter+"center="+lat+','+lng+'&';
				        })
				    .replace(
				    	// set the marker to the new location
				        /(\?|&)markers=((?:[^\|]*\|)*)[0-9\.\-]+,[0-9\.\-]+(&|$)/i,
				        function(match, delimiter, markerStyle) {
				          return delimiter+"markers="+markerStyle+lat+','+lng+'&';
				        })
				     );
		    M.gmap.switchImage(newImageSrc);
		},
		setZoom: function(newZoomLevel) {
			function replaceZoomLevel(uri, z) {
				return (
					uri.replace(
						zoomRE,
						function(match, startDelimiter, parameter, currentValue,
								 endDelimiter) {
					      		return (
					      			startDelimiter + parameter + "=" +
					      		    z.toString() + endDelimiter
					      		);
				        })
				    );
			}
		    var map = $('#map img'),
			    currentImageSrc = map.attr('src'),
				currentZoomOutURI = $('#zoom-out').attr('href'),
				currentZoomInURI = $('#zoom-in').attr('href'),
				currentGmapURI = $('#gmap-link').attr('href');
			
			document.cookie = 'zoom='+newZoomLevel.toString();
			M.gmap.switchImage(replaceZoomLevel(currentImageSrc, newZoomLevel));
			$('#zoom-out').attr('href', replaceZoomLevel(currentZoomOutURI, newZoomLevel - 1));
			$('#zoom-in').attr('href', replaceZoomLevel(currentZoomInURI, newZoomLevel + 1));
			$('#gmap-link').attr('href', replaceZoomLevel(currentGmapURI, newZoomLevel));
		}
	};
	
	$(function() {
	    $('#zoom-out').bind('click tap', function(e) {
	        e.preventDefault();
	        var currentZoom = zoomRE.exec($(this).attr('href')),
	        	newZoom = parseInt(currentZoom[3], 10);
	        M.gmap.setZoom(newZoom);
	    });
	    $('#zoom-in').bind('click tap', function(e) {
		    e.preventDefault();
		    var currentZoom = zoomRE.exec($(this).attr('href')),
		        newZoom = parseInt(currentZoom[3], 10);
		    M.gmap.setZoom(newZoom);
	    });
	});
}(jQuery));