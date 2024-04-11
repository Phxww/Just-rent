fetch("http://127.0.0.1:5000/api/cars")
  .then((response) => response.json())
  .then((data) => {
    const carsContainer = document.getElementById("cars-container");
    data
      .forEach((car) => {
        const carHtml = `
        <div class="card">
            <img src="https://fakeimg.pl/250/" class="card-img-top" alt="Car image"
                style="height: 200px;">
            <div class="card-body">
                <h5 class="card-title"> ${car.name}</h5>
                <p class="card-text"><i class="fas fa-heart"></i> 25 Likes</p>
                <p class="card-text">
                    <span class="badge bg-primary"><i class="fas fa-user"></i> ${car.model}</span>
                    <span class="badge bg-secondary"><i class="fas fa-suitcase"></i> ${car.model}</span>
                    <span class="badge bg-success"><i class="fas fa-car"></i> ${car.model}</span>
                </p>
                <p class="card-text">Daily rate from <strong>$265</strong></p>
                <a href="#" class="btn btn-primary">Rent Now</a>
            </div>
        </div>

        `;
        carsContainer.innerHTML = carHtml;
      })
      .catch((error) => console.error("Error fetching cars:", error));
  });
