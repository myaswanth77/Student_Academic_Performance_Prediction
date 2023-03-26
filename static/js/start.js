setTimeout(function() {
    document.getElementById("slide-text").style.top = "50%";
}, 500);

$(document).ready(function(){
    $('.nav-link').click(function(){
      $('.nav-link').removeClass('active');
      $(this).addClass('active');
    });
  });
  
  
  setTimeout(function() {
    $('#alert-message').fadeOut('fast');
  }, 3000);

