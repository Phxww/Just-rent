fetch(`/api/cars/${carId}`)
  .then((response) => response.json())
  .then((car) => {
    // Assuming response.json() returns a car object directly
    const carsSpec = document.getElementById("car-spec");
    const carHtml = `
            <h3>${car.name}</h3>
            <h2> Price: ${car.price} / day</h2>
            <h4>Specifications</h4>
            <ul class="list-unstyled">
                <li><strong>Body:</strong> ${car.body}</li>
                <li><strong>Seat:</strong> ${car.seat}</li>
            </ul>
        `;
    carsSpec.innerHTML = carHtml;
  })
  .catch((error) => console.error("Error fetching car:", error));
