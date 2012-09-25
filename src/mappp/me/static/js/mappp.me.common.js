/*jslint unparam: true, white: true, browser: true */
/* global google: true, jQuery: true*/
(function ($) {
	"use strict";
	
	window.mappp = window.mappp || {};
	var M = window.mappp.me = window.mappp.me || {};
	
	M.error = function(message) {
	  if (!$('#error').length) {
	    $('<a id="error"/>')
	        .hide()
	        .prependTo('#content');
	  }
	  $('#error')
	      .html('<span>'+message+'</span>')
	      .slideDown()
	      .click(function() {
	    	  $(this).slideUp();
	      });
	};
	M.hideError = function(message) {
	  $('#error').slideUp();
	};
	
	M.location = {
	  handleNoGeoLocation: function (browserSupportFlag) {
	    M.error('Could not get your location.');
	  },
	  getCurrentLocation: function(callback, errorCallback) {
		var browserSupportFlag = false, gearsGeo;
	    if (navigator.geolocation) {
	      browserSupportFlag = true;
	      navigator.geolocation.getCurrentPosition(function(position) {
	        var lat = position.coords.latitude,
	            lng = position.coords.longitude;
	        callback(lat, lng);
	      }, function() {
	        (errorCallback || M.location.handleNoGeoLocation)(browserSupportFlag);
	      },
	      {enableHighAccuracy: true,
	       timeout: 30000});
	    // Try Google Gears Geolocation
	    } else if (google.gears) {
	      browserSupportFlag = true;
	      gearsGeo = google.gears.factory.create('beta.geolocation');
	      gearsGeo.getCurrentPosition(function(position) {
	        var lat = position.latitude,
	            lng = position.longitude;
	        callback(lat, lng);
	      }, function() {
	        (errorCallback || M.location.handleNoGeoLocation)(browserSupportFlag);
	      });
	    } else {
	      (errorCallback || M.location.handleNoGeoLocation)(false);
	    }
	  }
	};
	
	$(function(){
	  $('.no-js').hide();
	  $('.js-only').show();
	  $('.button.js-only').css('display', 'inline-block');
	});
}(jQuery));