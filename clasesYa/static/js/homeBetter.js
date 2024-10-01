const inicioSlide = document.querySelector(".slideInicio");
const perfilSlide = document.querySelector(".slidePerfil");

function toggleSlide(slideToShow, ...slidesToHide) {
  document.body.classList.add("animating");
  slideToShow.style.display = "block";
  setTimeout(() => {
    slideToShow.classList.add("show");
    slidesToHide.forEach((slide) => {
      slide.style.display = "none";
      slide.classList.remove("show");
    });
    setTimeout(() => document.body.classList.remove("animating"), 550);
  }, 0);
}

document.getElementById("btnSlideInicio").addEventListener("click", () => {
  toggleSlide(inicioSlide, perfilSlide);
});

document.getElementById("btnSlidePerfil").addEventListener("click", () => {
  toggleSlide(perfilSlide, inicioSlide);
});

