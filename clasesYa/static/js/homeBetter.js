document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("liveToast");
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
});

const inicioSlide = document.querySelector(".slideInicio");
const miAnuncioSlide = document.querySelector(".slideMiAnuncio");
const perfilSlide = document.querySelector(".slidePerfil");

function toggleSlide(slideToShow, ...slidesToHide) {
  
  document.body.classList.add("animating");
  slideToShow.style.display = "block";
  setTimeout(() => {
    slidesToHide.forEach((slide) => {
      slide.style.display = "none";
      slide.classList.remove("show");
    });
    slideToShow.classList.add("show");
    setTimeout(() => document.body.classList.remove("animating"), 500);
  }, 0);
}

document.getElementById("btnSlideInicio").addEventListener("click", () => {
  toggleSlide(inicioSlide, perfilSlide, miAnuncioSlide);
});

document.getElementById("btnSlidePerfil").addEventListener("click", () => {
  toggleSlide(perfilSlide, inicioSlide, miAnuncioSlide);
});

document.getElementById("btnSlideMiAnuncio").addEventListener("click", () => {
  toggleSlide(miAnuncioSlide, inicioSlide, perfilSlide);
});