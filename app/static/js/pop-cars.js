fetch("/api/cars/pop")
  .then((response) => response.json())
  .then((data) => {
    const carsContainer = document.getElementById("cars-container");

    data.forEach((car) => {
      const imageName = encodeURIComponent(
        car.name
      );

      const imageUrl = `../static/crawler/${imageName}/img_2.jpg`; // Update the extension if different
      const carHtml = `
        <div class="col-md-4 mb-4">
          <div class="card h-100">
              <span class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
              Hot!
          </span>
            <img class="card-img-top" src="${imageUrl}" alt="${car.name}">
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
                      <span class="text-muted original-price">$ ${car.price}</span>
                      <br>
                      <span class="discounted-price ms-2"> 3 days <del>$ ${car.original_price} </del>$ ${car.discount_price} </span>
                    </p>
                  </div>
                  <div class="col text-center">
                    <a href="/cars/${car.id}" class="btn btn-primary">Check</a>
                  </div>
                </div>
              </div>
          </div>
          </div>
        </div>
      `;
      carsContainer.innerHTML += carHtml;
    });
  })
  .catch((error) => console.error("Error fetching cars:", error));
