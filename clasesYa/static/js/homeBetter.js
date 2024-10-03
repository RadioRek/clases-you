document.addEventListener("DOMContentLoaded", function () {
  var toastEl = document.getElementById("liveToast");
  var toast = new bootstrap.Toast(toastEl);
  toast.show();
});

const inicioSlide = document.querySelector(".slideInicio");
const perfilSlide = document.querySelector(".slidePerfil");

function toggleSlide(slideToShow, ...slidesToHide) {
  if (document.body.classList.contains("animating")) return;
  document.body.classList.add("animating");
  slideToShow.style.display = "block";
  setTimeout(() => {
    slideToShow.classList.add("show");
    slidesToHide.forEach((slide) => {
      slide.style.display = "none";
      slide.classList.remove("show");
    });
    setTimeout(() => document.body.classList.remove("animating"), 500);
  }, 0);
}

document.getElementById("btnSlideInicio").addEventListener("click", () => {
  toggleSlide(inicioSlide, perfilSlide);
});

document.getElementById("btnSlidePerfil").addEventListener("click", () => {
  toggleSlide(perfilSlide, inicioSlide);
});
