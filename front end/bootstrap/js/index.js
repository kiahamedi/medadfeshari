$(document).ready(function() {
     
    $("#owl-example").owlCarousel({
      	'items' : 1,
      	'itemsDesktop':1,
      	'itemsDesktopSmall':1,
      	'itemsTablet':1,
      	'itemsMobile':1,
      	'navigation':true,
      	'pagination':true,
      	'navigationText':["داستان قبلی","داستان بعدی"]
    });        
});

$('.step .one .arrow i').click(function(){
    $(this).toggleClass('actives');
    $(this).parents('.step').find('.author').slideToggle(150);
});