fetch(`/api/cars/${carId}`)
  .then((response) => response.json())
  .then((car) => {
    // Assuming response.json() returns a car object directly
    const carsSpec = document.getElementById("spec-table-body");
    const carHtml = `
    <tr>
        <th>Name</th>
        <td>${car.name}</td>
    </tr>
    <tr>
        <th>Price / day</th>
        <td>$ ${car.price}</td>
    </tr>
    <tr>
        <th>Body</th>
        <td>${car.body}</td>
    </tr>
    <tr>
        <th>Seat</th>
        <td>${car.seat}</td>
    </tr>
    <tr>
        <th>Door</th>
        <td>${car.door}</td>
    </tr>
        </tr>
    <tr>
        <th>Displacement</th>
        <td>${car.displacement}</td>
    </tr>
        </tr>
    <tr>
        <th>Wheelbase</th>
        <td>${car.wheelbase}</td>
    </tr>
     <tr>
        <th>Power type</th>
        <td>${car.power_type}</td>
    </tr>
`;
    carsSpec.innerHTML = carHtml;
  })
  .catch((error) => console.error("Error fetching car:", error));
