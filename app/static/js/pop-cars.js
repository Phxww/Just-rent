fetch("/api/cars/pop")
  .then((response) => response.json())
  .then((data) => {
    const carsContainer = document.getElementById("cars-container");

    data
      .forEach((car) => {
        const carHtml = `
        <div class="col-md-4 mb-4">
          <div class="card h-100">
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              Hot!
          </span>
            <img class="card-img-top" src="https://fakeimg.pl/250/" alt="Car 1">
            <div class="card-body">
              <h5 class="card-title">${car.name}</h5>
                <p class="card-text">
                  <strong class="me-2">Seat:</strong><span>${car.seat}</span><br>
                  <strong class="me-2">Door:</strong><span>${car.door}</span><br>
                  <strong class="me-2">Body:</strong><span>${car.body}</span>
                </p>
            </div>
              <div class="card-footer">
                <div class="row align-items-center">
                  <div class="col text-center">
                    <p class="card-text">
                      <strong>Daily price:</strong><span></span>
                      <span class="text-muted original-price"><del>$300</del></span>
                      <span class="discounted-price ms-2">$265</span>
                    </p>
                  </div>
                  <div class="col text-center">
                    <a href="#" class="btn btn-primary">Rent Now</a>
                  </div>
                </div>
              </div>
          </div>
          </div>
        </div>
      `;
        carsContainer.innerHTML += carHtml;
      })
      .catch((error) => console.error("Error fetching cars:", error));
  });
