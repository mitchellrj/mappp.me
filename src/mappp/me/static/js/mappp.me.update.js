window.mappp = window.mappp || {};
window.mappp.me = window.mappp.me || {};

window.mappp.me.following = false;

window.mappp.me.update = {
  noLocation: function (browserSupport) {
    if (!browserSupport) {
      window.mappp.me.error('Your device either does not support geolocation, or does not have geolocation enabled.');
    } else {
      window.mappp.me.error("We couldn't get your location for some reason.");
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
      'success': mappp.me.update.updateSessionSuccess,
      'error': mappp.me.update.updateSessionError
      });
  },
  updateSessionSuccess: function(data, textStatus, xhr) {
    $('#update-button span').html("Update now");
    $('#last-updated').html(data.last_updated);
    mappp.me.hideError();
    mappp.me.gmap.updateLocation(data.latitude, data.longitude);
  },
  updateSessionError: function(xhr, textStatus, error) {
    mappp.me.error('Location update failed:\n' + error);
  }
};

window.mappp.me.follow = function() {
  if (mappp.me.following) {
    mappp.me.location.getCurrentLocation(
        window.mappp.me.follow.followCallback,
        window.mappp.me.follow.followErrorCallback);
    var timeout = parseFloat($('#update-interval').val())*60000;
    if (timeout>0) { // also catches NaN
      window.setTimeout(window.mappp.me.follow, timeout);
    }
  }
};

window.mappp.me.follow.followCallback = function(lat, lng) {
  mappp.me.hideError();
  if (mappp.me.following) {
    window.mappp.me.update.locationCallback(lat, lng);
  }
};

$(function() {
  function decreaseFrequency (e) {
    if (e.type==='keyup' && (parseInt(e.keyCode)!==13 && parseInt(e.keyCode)!==20)) {
      return;
    }
    var currentVal = parseFloat($('#update-interval').val());
    if (currentVal>0) { // also catches NaN
      e.preventDefault();
      var step = currentVal <= 1 ? 0.5 : (currentVal <= 5 ? 1 : (currentVal <= 30 ? 5 : 10));
      $('#update-interval').val(Math.max(0.5, currentVal-step));
    }
  }
  function increaseFrequency(e) {
    if (e.type==='keyup' && (parseInt(e.keyCode)!==13 && parseInt(e.keyCode)!==20)) {
      return;
    }
    var currentVal = parseFloat($('#update-interval').val());
    if (currentVal>0) { // also catches NaN
      e.preventDefault();
      var step = currentVal < 1 ? 0.5 : (currentVal < 5 ? 1 : (currentVal < 30 ? 5 : 0));
      $('#update-interval').val(currentVal+step);
    }
  }
  function doUpdate(e) {
    if (e.type==='keyup' && (parseInt(e.keyCode)!==13 && parseInt(e.keyCode)!==20)) {
      return;
    }
    e.preventDefault();
    $('#update-button span').html("Updating...");
    mappp.me.location.getCurrentLocation(
        window.mappp.me.update.locationCallback,
        window.mappp.me.update.noLocation);
    _gaq.push(['_trackEvent', 'Mappps', 'Updated']);
  }
  function toggleFollow(e) {
    if (e.type==='keyup' && (parseInt(e.keyCode)!==13 && parseInt(e.keyCode)!==20)) {
      return;
    }
    e.preventDefault();
    if (mappp.me.following) {
      mappp.me.following = false;
      $('span', this).html("Follow me");
      $('#update-interval-form').slideToggle();
      _gaq.push(['_trackEvent', 'Mappps', 'Stop following']);
    } else {
      $('span', this).html("Stop following");
      $('#update-interval-form').slideToggle();
      mappp.me.following = true;
      window.mappp.me.follow();
      _gaq.push(['_trackEvent', 'Mappps', 'Start following']);
    }
  }
  $('#update-button').bind('click tap', doUpdate);
  $('#follow-button').bind('click tap', toggleFollow);
  $('input[name=decrease_frequency]').bind('click tap', decreaseFrequency);
  $('input[name=increase_frequency]').bind('click tap', increaseFrequency);
  $('#delete-button').bind('click tap', function() {
      _gaq.push(['_trackEvent', 'Mappps', 'Delete']);
  });
});
