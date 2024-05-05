function favoriteCar() {
  fetch("/api/favorites")
    .then((response) => response.json())
    .then((data) => {
      const tableBody = document.querySelector(".table tbody");
      tableBody.innerHTML = ""; 

      data.forEach((car) => {
        const row = document.createElement("tr"); 
        row.innerHTML = `
          <td><span class="d-lg-none d-sm-block">Car ID</span>
              <div class="bg-gray-100 text-dark">${car.id}</div>
          </td>
          <td><span class="d-lg-none d-sm-block">Car Name</span><span class="bold">${car.name}</span></td>
          <td><span class="d-lg-none d-sm-block">Daily rate</span>$${car.price}</td>
          <td>
              <a href="/cars/${car.id}" class="btn btn-primary">Check</a>
          </td>
        `;
        tableBody.appendChild(row); // Append the new row to the table body
      });
    })
    .catch((error) => console.error("Error fetching favorite cars:", error));
}

function rentNow(carId) {
  console.log("Renting car:", carId);
  // Additional functionality to handle car renting
}

document.addEventListener("DOMContentLoaded", favoriteCar);
