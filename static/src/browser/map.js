(function( $ ){

  $.staticMap = function( options ){

    var defaults = {
      zoom : 3,
      width: 300,//image width
      height: 300,//image height
      address: 'USA', //could be string address or lat,lon("-3.444,3.222")
      markerIcon: '', //url to custom icon
      key: '',// google map key
      sensor: false,
      mapType: 'roadmap',//map type []
      scale: 1 // helps when need map on mobile, need change scale to 2
    };

    var settings = $.extend( {}, defaults, options );

    var url = 'http://maps.googleapis.com/maps/api/staticmap?';
    if(settings.key != ''){
      url += 'key='+settings.key+'&';
    }//if
    url += 'center='+settings.address+'&';
    url += 'zoom='+settings.zoom+'&';
    url += 'size='+settings.width+'x'+settings.height+'&';
    url += 'markers=';
    if(settings.markerIcon != ''){
      url +='icon:'+settings.markerIcon+'|';
    }
    url += settings.address+'&';
    url += 'maptype='+settings.mapType+'&';
    url += 'scale='+settings.scale+'&';
    url += 'sensor='+settings.sensor;

    return url;

  }//map

  $.liveMapLink = function( options ){

    var defaults = {
      address: '',
      zoom: 5
    };

    var settings = $.extend( {}, defaults, options );

    var url = 'https://maps.google.com/?q=';
    
    url += settings.address + '&';
    url += 'z=' + settings.zoom;
    return url;

  }//map


})( jQuery );
