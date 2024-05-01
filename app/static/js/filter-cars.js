function loadBrands() {
  fetch("/api/brand") 
    .then((response) => response.json())
    .then((brands) => {
      const brandFilter = document.getElementById("brand-filter");
      brands.forEach((brand) => {
        const option = document.createElement("option");
        option.value = brand;
        option.textContent = brand;
        brandFilter.appendChild(option);
      });
    })
    .catch((error) => console.error("Failed to load brands:", error));
}
function loadSeats() {
  fetch("/api/seat")
    .then((response) => response.json())
    .then((seats) => {
      const seatFilter = document.getElementById("seats-filter");
      seats.forEach((seat) => {
        const option = document.createElement("option");
        option.value = seat;
        option.textContent = seat;
        seatFilter.appendChild(option);
      });
    })
    .catch((error) => console.error("Failed to load seats:", error));
}

function loadDoors() {
  fetch("/api/door")
    .then((response) => response.json())
    .then((doors) => {
      const doorFilter = document.getElementById("doors-filter");
      doors.forEach((door) => {
        const option = document.createElement("option");
        option.value = door;
        option.textContent = door;
        doorFilter.appendChild(option);
      });
    })
    .catch((error) => console.error("Failed to load doors:", error));
}

function loadPower() {
  fetch("/api/power")
    .then((response) => response.json())
    .then((powers) => {
      const powerFilter = document.getElementById("power-filter");
      powers.forEach((power) => {
        const option = document.createElement("option");
        option.value = power;
        option.textContent = power;
        powerFilter.appendChild(option);
      });
    })
    .catch((error) => console.error("Failed to load power type:", error));
}


document.addEventListener("DOMContentLoaded", loadBrands);
document.addEventListener("DOMContentLoaded", loadSeats);
document.addEventListener("DOMContentLoaded", loadDoors);
document.addEventListener("DOMContentLoaded", loadPower);