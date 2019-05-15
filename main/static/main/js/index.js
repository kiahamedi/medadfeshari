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
       'navigationText':["ﺩاﺳﺘﺎﻥ ﻗﺒﻞی","ﺩاﺳﺘﺎﻥ ﺑﻌﺪی"]
    });        

});

// $('.step .one .arrow i').click(function(){
//     $(this).toggleClass('actives');
//     $(this).parents('.step').find('.author').slideToggle(150);
// });


// $(function(){

//    $('#submitinput').click(function(){
//       var nameContent = $('#nameinput').val();
//       var emailContent = $('#emailinput').val();
//       var priceContent = $('#priceinput').val();
//            if(nameContent == ''){
//               $('.messagebox').fadeIn('slow').delay(2000).fadeOut('.messagebox');                
//             }else if(emailContent == ''){
//               $('.messagebox').fadeIn('slow').delay(2000).fadeOut('.messagebox');
//             }else if(priceContent == ''){
//               $('.messagebox').fadeIn('slow').delay(2000).fadeOut('.messagebox');
//             }            
//    });

// });

$('.btn-support').click(function(){
      $('.support-table').slideToggle(500);
    });

