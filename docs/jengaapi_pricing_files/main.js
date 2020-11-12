AOS.init({
  easing: 'ease-in-out-sine',
  duration: 1200
});

//Dropdown Script

$(function(){
$(".dropdown").hover(            
  function() {
      $('.dropdown-menu', this).stop( true, true ).fadeIn("fast");
      $(this).toggleClass('open');
      $('b', this).toggleClass("caret caret-up");                
  },
  function() {
      $('.dropdown-menu', this).stop( true, true ).fadeOut("fast");
      $(this).toggleClass('open');
      $('b', this).toggleClass("caret caret-up");                
  });
});

//Shop tab
 $(".tab-list li").click(function() {
        $(".tab-list li").removeClass('active');
        $(this).addClass('active');
        $('.tab-content').hide().eq($(this).index()).fadeIn(300);
    });
$('.tab-list > li').first().click();

//Shop tab2
 $(".tab-list2 li").click(function() {
        $(".tab-list2 li").removeClass('active');
        $(this).addClass('active');
        $('.tab-content2').hide().eq($(this).index()).fadeIn(300);
    });
$('.tab-list2 > li').first().click();

$('.nav-tabs-dropdown').each(function(i, elm) {
    
    $(elm).text($(elm).next('ul').find('li.active a').text());
    
});