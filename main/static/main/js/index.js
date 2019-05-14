    $(document).ready(function() {
     
     function removeAlert(){
            $('.fadeoutalertsuc').fadeOut(5000);

            $('.fadeoutalertinfo').fadeOut(5000);

            $('.fadeoutalertwarnin').fadeOut(5000);

            $('.fadeoutalerterror').fadeOut(5000);
            }

           removeAlert();

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