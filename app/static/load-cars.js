fetch("/api/cars")
  .then((response) => response.json())
  .then((data) => {
    const carsContainer = document.getElementById("cars-container");
    data
      .forEach((car) => {
        const carHtml = `
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="card">
            <img src="https://fakeimg.pl/250/" class="card-img-top" alt="Car image"
                style="height: 200px;">
              <div class="card-body">
                  <h5 class="card-title"> ${car.name}</h5>
                  <p class="card-text"><i class="fas fa-heart"></i> 25 Likes</p>
                  <p class="card-text">
                      <strong class="me-2">Brand:</strong><span>${car.brand}</span><br>
                      <strong class="me-2">Year:</strong><span>${car.year}</span><br>
                      <strong class="me-2">Model:</strong><span>${car.model}</span>
                  </p>
                  <p class="card-text">Daily rate from <strong>$265</strong></p><br>
                  <a href="#" class="btn btn-primary">Rent Now</a>
              </div>
          </div>
        </div>
        `;
        carsContainer.innerHTML += carHtml;
      })
      .catch((error) => console.error("Error fetching cars:", error));
  });
