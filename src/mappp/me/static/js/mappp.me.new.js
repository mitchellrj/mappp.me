window.mappp = window.mappp || {};
window.mappp.me = window.mappp.me || {};

window.mappp.me.new_ = {
  noLocation: function (browserSupport) {
    if (!browserSupport) {
      alert('Your device either does not support geolocation, or does not have geolocation enabled. Check your device settings.');
    } else {
      alert("We couldn't get your location for some reason. Check your browser settings.");
    }
    $('#new-session span').html("New mappp");
  },
  locationCallback: function (lat, lng) {
    $('#new-session span').html("Creating mappp...");
    $.ajax({
      'url': document.location + 'new',
      'dataType': 'json',
      'data': {'latitude': lat,
               'longitude': lng,
               'tz': (new Date()).getTimezoneOffset()
               },
      'type': 'POST',
      'success': mappp.me.new_.newSessionSuccess,
      'error': mappp.me.new_.newSessionError
      });
  },
  newSessionSuccess: function(data, textStatus, xhr) {
    if (data.admin_link) {
      $('#new-session span').html("Loading location...");
      window.location = data.admin_link;
    } else {
      $('#new-session span').html("New mappp");
      alert('Error!');
    }
  },
  newSessionError: function(xhr, textStatus, error) {
    $('#new-session span').html("New mappp");
    alert('Could not start a session at this time.\n'+error);
  }
};

$(function() {
  $('#new-session').bind('click tap', function(e) {
    e.preventDefault();
    e.stopPropagation();
    $('#new-session span').html("Getting location...");
    mappp.me.location.getCurrentLocation(mappp.me.new_.locationCallback,
                                         mappp.me.new_.noLocation);
    _gaq.push(['_trackEvent', 'Mappps', 'New']);
    return false;
  });
  $('.existing-mappp').click(function() {
    _gaq.push(['_trackEvent', 'Mappps', 'Return to existing']);
  });
});