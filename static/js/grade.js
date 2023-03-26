document.addEventListener("DOMContentLoaded", function() {
    var navLinks = document.getElementsByClassName("nav-link");
    if (navLinks.length) {
      for (var i = 0; i < navLinks.length; i++) {
        navLinks[i].addEventListener("click", function() {
          for (var j = 0; j < navLinks.length; j++) {
            navLinks[j].classList.remove("active");
          }
          this.classList.add("active");
        });
      }
    }
  });
  
  
  $(window).on("scroll", function() {
    if ($(window).scrollTop() > 100) {
        $(".content").addClass("hide");
    } else {
        $(".content").removeClass("hide");
    }
  });
  
  
  
    const marks = document.getElementById("marks");
    const radio12th = document.getElementById("12th");
    const radioDiploma = document.getElementById("diploma");
    const rank = document.getElementById("Rank");
    const radioeamcet = document.getElementById("Eamcet");
    const radioecet = document.getElementById("Ecet");
    
    radio12th.addEventListener("change", function() {
      marks.min = 1;
      marks.max = 1000;
    });
  
    radioDiploma.addEventListener("change", function() {
      marks.min = 1;
      marks.max = 600;
    });
  
    radioeamcet.addEventListener("change", function() {
      marks.min = 1;
      marks.max = 100000;
    });
  
    radioecet.addEventListener("change", function() {
      marks.min = 1;
      marks.max = 100000;
    });
    
  
  
  
  
  
  
  
  
  