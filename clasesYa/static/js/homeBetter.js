const inicioSlide = document.querySelector(".slideInicio");
const perfilSlide = document.querySelector(".slidePerfil");
const configuracionSlide = document.querySelector(".slideConfiguracion");
const acercaDeSlide = document.querySelector(".slideAcercaDe");

function toggleSlide(slideToShow, ...slidesToHide) {
  slideToShow.style.display = "block";
  setTimeout(() => {
    slideToShow.classList.add("show");
    slidesToHide.forEach((slide) => {
      slide.style.display = "none";
      slide.classList.remove("show");
    });
  }, 0);
}

document.getElementById("btnSlideInicio").addEventListener("click", () => {
  toggleSlide(inicioSlide, perfilSlide, configuracionSlide, acercaDeSlide);
});

document.getElementById("btnSlidePerfil").addEventListener("click", () => {
  toggleSlide(perfilSlide, inicioSlide, configuracionSlide, acercaDeSlide);
});

document
  .getElementById("btnSlideConfiguracion")
  .addEventListener("click", () => {
    toggleSlide(configuracionSlide, inicioSlide, perfilSlide, acercaDeSlide);
  });

document.getElementById("btnSlideAcercaDe").addEventListener("click", () => {
  toggleSlide(acercaDeSlide, inicioSlide, perfilSlide, configuracionSlide);
});
