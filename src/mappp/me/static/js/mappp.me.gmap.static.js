window.mappp = window.mappp || {};
window.mappp.me = window.mappp.me || {};

window.mappp.me.gmap = {
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
    var map = $('#map img');
    var currentImageSrc = map.attr('src');
    var newImageSrc = currentImageSrc.replace(
        /(\?|&)center=[0-9\.-]+,[0-9\.-]+(&|$)/i,
        function(match, delimiter) {
          return delimiter+"center="+lat+','+lng+'&';
        }).replace(
        /(\?|&)markers=((?:[^\|]*\|)*)[0-9\.-]+,[0-9\.-]+(&|$)/i,
        function(match, delimiter, markerStyle) {
          return delimiter+"markers="+markerStyle+lat+','+lng+'&';
        });
    mappp.me.gmap.switchImage(newImageSrc);
  },
  setZoom: function(newZoom) {
    var map = $('#map img');
    var currentImageSrc = map.attr('src');
    var matcher = /(\?|&)(z(oom)?)=(\d+)($|&)/i;
    var newImageSrc = currentImageSrc.replace(
        matcher,
        function(match, delimiter, term) {
          return delimiter+term+"="+newZoom+'&';
        });

    mappp.me.gmap.switchImage(newImageSrc);
    document.cookie = 'zoom='+newZoom;
    $('#zoom-out').attr('href', $('#zoom-out').attr('href').replace(matcher, function(match, delimiter) { return delimiter + 'zoom=' + (newZoom - 1) + '&'; }));
    $('#zoom-in').attr('href', $('#zoom-in').attr('href').replace(matcher, function(match, delimiter) { return delimiter + 'zoom=' + (newZoom + 1) + '&'; }));
    $('#gmap-link').attr('href', $('#gmap-link').attr('href').replace(matcher, function(match, delimiter) { return delimiter + 'z=' + (newZoom) + '&'; }));
  }
};

$(function() {
  $('#zoom-out').bind('click tap', function(e) {
    e.preventDefault();
    var currentZoom = /(&|\?)zoom=(\d+)($|&)/i.exec($(this).attr('href'));
    var newZoom = parseInt(currentZoom[2]);
    mappp.me.gmap.setZoom(newZoom);
  });
  $('#zoom-in').bind('click tap', function(e) {
    e.preventDefault();
    var currentZoom = /(&|\?)zoom=(\d+)($|&)/.exec($(this).attr('href'));
    var newZoom = parseInt(currentZoom[2]);
    mappp.me.gmap.setZoom(newZoom);
  });
});