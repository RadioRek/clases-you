/*
https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}&lang={lang}
*/
apiKey = "f06df6c10438672250e6ed34b9956af8";
idioma = "sp";

function getLocation() {
  return new Promise((resolve, reject) => {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        function (position) {
          resolve({
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          });
        },
        function (error) {
          reject(error);
        }
      );
    } else {
      reject(new Error("Geolocation is not supported by this browser."));
    }
  });
}

getLocation()
  .then((location) => {
    let apiUrl = `https://api.openweathermap.org/data/2.5/weather?lat=${location.latitude}&lon=${location.longitude}&appid=${apiKey}&lang=${idioma}&units=metric`;
    // Fetch the weather data
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        let weather = data.weather[0].description;
        let temperature = data.main.temp;
        let city = data.name;
        let country = data.sys.country;
        let icon = data.weather[0].icon;

        document.getElementById(
          "tiempo"
        ).innerHTML = `<img src="http://openweathermap.org/img/wn/${icon}.png"> ${temperature}°C ${weather}, ${city} ${country}`;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  })
  .catch((error) => {
    console.error("Error:", error);
  });
