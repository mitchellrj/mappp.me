/*jslint nomen: true, unparam: true, white: true, browser: true */
/* global jQuery: true, google: true, _gaq: true */
(function($) {
	"use strict";

	window.mappp = window.mappp || {};
	var M = window.mappp.me = window.mappp.me || {};
	
	M.following = false;
	
	M.update = {
	  noLocation: function (browserSupport) {
	    if (!browserSupport) {
	      M.error('Your device either does not support geolocation, or ' +
	    		  'does not have geolocation enabled.');
	    } else {
	      M.error("We couldn't get your location for some reason.");
	    }
	    $('#update-button span').html("Update now");
	  },
	  locationCallback: function (lat, lng) {
	    $.ajax({
	      'url': document.location,
	      'dataType': 'json',
	      'data': {'latitude': lat,
	               'longitude': lng
	               },
	      'type': 'POST',
	      'success': M.update.updateSessionSuccess,
	      'error': M.update.updateSessionError
	      });
	  },
	  updateSessionSuccess: function(data, textStatus, xhr) {
	    $('#update-button span').html("Update now");
	    $('#last-updated').html(data.last_updated);
	    M.hideError();
	    M.gmap.updateLocation(data.latitude, data.longitude);
	  },
	  updateSessionError: function(xhr, textStatus, error) {
	    M.error('Location update failed:\n' + error);
	  }
	};
	
	M.follow = function() {
	  if (M.following) {
	    M.location.getCurrentLocation(
	        M.follow.followCallback,
	        M.follow.followErrorCallback);
	    var timeout = parseFloat($('#update-interval').val())*60000;
	    if (timeout>0) { // also catches NaN
	      window.setTimeout(M.follow, timeout);
	    }
	  }
	};
	
	M.follow.followCallback = function(lat, lng) {
	  M.hideError();
	  if (M.following) {
	    M.update.locationCallback(lat, lng);
	  }
	};
	
	$(function() {
	  var enterOrSpace = function (keyCode) {
		  keyCode = parseInt(keyCode, 10);
		  return keyCode===13 || keyCode===20;
	  },
	  getStep = function (currentValue) {
		  var step = 10;
		  if (currentValue <= 1) {
			  step = 0.5;
		  } else if (currentValue <= 5) {
			  step = 1;
		  } else if (currentValue <= 30) {
			  step = 5;
		  }
		  return step;
	  },
	  decreaseFrequency = function (e) {
	    if (e.type==='keyup' && !enterOrSpace(e.keyCode)) {
	      return;
	    }
	    var currentVal = parseFloat($('#update-interval').val()),
	        step = getStep(currentVal);
	    if (currentVal>0) { // also catches NaN
	      e.preventDefault();
	      $('#update-interval').val(Math.max(0.5, currentVal-step));
	    }
	  },
	  increaseFrequency = function (e) {
	    if (e.type==='keyup' && !enterOrSpace(e.keyCode)) {
	      return;
	    }
	    var currentVal = parseFloat($('#update-interval').val()),
	        step = getStep(currentVal);
	    if (currentVal>0) { // also catches NaN
	      e.preventDefault();
	      $('#update-interval').val(currentVal+step);
	    }
	  },
	  doUpdate = function (e) {
	    if (e.type==='keyup' && !enterOrSpace(e.keyCode)) {
	      return;
	    }
	    e.preventDefault();
	    $('#update-button span').html("Updating...");
	    M.location.getCurrentLocation(
	        M.update.locationCallback,
	        M.update.noLocation);
	    _gaq.push(['_trackEvent', 'Mappps', 'Updated']);
	  },
	  toggleFollow = function (e) {
	    if (e.type==='keyup' && !enterOrSpace(e.keyCode)) {
	      return;
	    }
	    e.preventDefault();
	    if (M.following) {
	      M.following = false;
	      $('span', this).html("Follow me");
	      $('#update-interval-form').slideToggle();
	      _gaq.push(['_trackEvent', 'Mappps', 'Stop following']);
	    } else {
	      $('span', this).html("Stop following");
	      $('#update-interval-form').slideToggle();
	      M.following = true;
	      M.follow();
	      _gaq.push(['_trackEvent', 'Mappps', 'Start following']);
	    }
	  };
	  $('#update-button').bind('click tap', doUpdate);
	  $('#follow-button').bind('click tap', toggleFollow);
	  $('input[name=decrease_frequency]').bind('click tap', decreaseFrequency);
	  $('input[name=increase_frequency]').bind('click tap', increaseFrequency);
	  $('#delete-button').bind('click tap', function() {
	      _gaq.push(['_trackEvent', 'Mappps', 'Delete']);
	  });
	});
}(jQuery));