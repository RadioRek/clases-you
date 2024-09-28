// variables
let inputPassword = document.querySelector("#inputPassword");
let inputConfirmarPassword = document.querySelector("#inputConfirmarPassword");
let termCheckBox = document.querySelector("#termCheckBox");
let privaCheckBox = document.querySelector("#privaCheckBox");
let botonRegistro = document.querySelector("#botonRegistro");

let errorPassword = document.querySelector("#errorPassword");
let errorTerminos = document.querySelector("#errorTerminos");
let errorPrivacidad = document.querySelector("#errorPrivacidad");

errorPassword.style.display = "none";
errorTerminos.style.display = "none";
errorPrivacidad.style.display = "none";

function checkValidity() {
  if (
    inputPassword.value === inputConfirmarPassword.value &&
    termCheckBox.checked &&
    privaCheckBox.checked
  ) {
    botonRegistro.disabled = false;
  } else {
    botonRegistro.disabled = true;
  }
}

checkValidity();

inputConfirmarPassword.addEventListener("input", () => {
  if (inputConfirmarPassword.value !== inputPassword.value) {
    errorPassword.style.display = "block";
  } else {
    errorPassword.style.display = "none";
  }
  checkValidity();
});

inputPassword.addEventListener("input", () => {
  if (inputConfirmarPassword.value !== inputPassword.value) {
    errorPassword.style.display = "block";
  } else {
    errorPassword.style.display = "none";
  }
  checkValidity();
});

termCheckBox.addEventListener("change", () => {
  if (!termCheckBox.checked) {
    errorTerminos.style.display = "block";
  } else {
    errorTerminos.style.display = "none";
  }
  checkValidity();
});

privaCheckBox.addEventListener("change", () => {
  if (!privaCheckBox.checked) {
    errorPrivacidad.style.display = "block";
  } else {
    errorPrivacidad.style.display = "none";
  }
  checkValidity();
});

function checkValidity() {
  if (
    inputPassword.value === inputConfirmarPassword.value &&
    termCheckBox.checked &&
    privaCheckBox.checked
  ) {
    botonRegistro.disabled = false;
  } else {
    botonRegistro.disabled = true;
  }
}
