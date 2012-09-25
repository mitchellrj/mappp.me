window.mappp = window.mappp || {};
window.mappp.me = window.mappp.me || {};

window.mappp.me.error = function(message) {
  if (!$('#error').length) {
    $('<a id="error"/>').hide().prependTo('#content');
  }
  $('#error').html('<span>'+message+'</span>').slideDown().click(function() { $(this).slideUp(); });
};
window.mappp.me.hideError = function(message) {
  $('#error').slideUp();
};

window.mappp.me.location = {
  handleNoGeoLocation: function (browserSupportFlag) {
    mappp.me.error('Could not get your location.');
  },
  getCurrentLocation: function(callback, errorCallback) {
    if (navigator.geolocation) {
      browserSupportFlag = true;
      navigator.geolocation.getCurrentPosition(function(position) {
        var lat = position.coords.latitude,
            lng = position.coords.longitude;
        callback(lat, lng);
      }, function() {
        (errorCallback || mappp.me.location.handleNoGeoLocation)(browserSupportFlag);
      },
      {enableHighAccuracy: true,
       timeout: 30000});
    // Try Google Gears Geolocation
    } else if (google.gears) {
      browserSupportFlag = true;
      var geo = google.gears.factory.create('beta.geolocation');
      geo.getCurrentPosition(function(position) {
        var lat = position.latitude,
            lng = position.longitude;
        callback(lat, lng);
      }, function() {
        (errorCallback || mappp.me.location.handleNoGeoLocation)(browserSupportFlag);
      });
    } else {
      (errorCallback || mappp.me.location.handleNoGeoLocation)(false);
    }
  }
};

$(function(){
  $('.no-js').hide();
  $('.js-only').show();
  $('.button.js-only').css('display', 'inline-block');
});