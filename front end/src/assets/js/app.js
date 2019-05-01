$(document).ready(function () {
  if ($('.diary-slider')) {
    $('.diary-slider').slick({
      dots: false,
      vertical: true,
      slidesToShow: 1,
      slidesToScroll: 1,
      verticalSwiping: true,
      infinite: true,
      arrows: true,
      focusOnSelect: true,
      autoplay: true,
      autoplaySpeed: 7000,
    });
  }

  $("header .menu-button").click(function () {
    $("html body").toggleClass("overflow-hidden");
    $("header .menu").toggleClass("open");
  });
});