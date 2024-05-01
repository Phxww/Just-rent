function loadPage(page) {
  window.scrollTo(0, 0);
  const brand = document.getElementById("brand-filter").value;
  const doors = document.getElementById("doors-filter").value;
  const seats = document.getElementById("seats-filter").value;
  const powerType = document.getElementById("power-filter").value;
  // const displacement = document.getElementById("displacement-filter").value;
  // const queryParams = new URLSearchParams({page, brand, doors, seats, powerType, displacement});
    const queryParams = new URLSearchParams({page, brand,seats,doors,powerType});
    console.log(queryParams.toString());
  fetch(`/api/cars?${queryParams.toString()}`)
  // fetch(`/api/cars?page=${page}`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      const carsContainer = document.getElementById("cars-container");
      carsContainer.innerHTML = ""; // clear the prvious page data
      data.cars.forEach((car) => {
        const carHtml = `
        <div class="col-lg-3 col-md-6 mb-4">
          <div class="card">
          <a href="/cars/${car.id}">
            <img src="https://fakeimg.pl/250/" class="card-img-top" alt="Car image"
                style="height: 200px;"></a>
              <div class="card-body">
                  <h6 class="card-title"><a href="/cars/${car.id}">${
          car.name
        }</a></h6>
                  <p class="card-text">
                      <i class="like-icon fas fa-heart ${
                        car.isLiked ? "liked" : ""
                      }" data-liked="${car.isLiked}" data-car-id="${
          car.id
        }"></i>
                  <p class="card-text">Daily rate from <strong>$ ${car.price}</strong></p><br>
              </div>
          </div>
        </div>
        `;
        carsContainer.innerHTML += carHtml;
      });
      setupPagination(data.current_page, data.total_pages);
      // Setup click handlers if not authenticated
      if (!data.isAuthenticated) {
        document.querySelectorAll(".like-icon").forEach((icon) => {
          icon.addEventListener("click", function () {
            window.location.href = "/login";
          });
        });
      }
    })
    .catch((error) => console.error("Error fetching cars:", error));
}

function setupPagination(currentPage, totalPages) {
  const paginationUl = document.getElementById("pagination");
  paginationUl.innerHTML = ""; // Clear previous pagination

  // Handle previous link
  const prevLi = `<li class="page-item ${currentPage === 1 ? "disabled" : ""}">
                      <button class="page-link" onclick="loadPage(${currentPage - 1})">Previous</button>
                   </li>`;
  paginationUl.innerHTML += prevLi;

  // Generate page numbers
  for (let i = 1; i <= totalPages; i++) {
    paginationUl.innerHTML += `<li class="page-item ${
      i === currentPage ? "active" : ""
    }">
                                       <button class="page-link" onclick="loadPage(${i})">${i}</button>
                                   </li>`;
  }

  // Handle next link
  const nextLi = `<li class="page-item ${
    currentPage === totalPages ? "disabled" : ""
  }">
                       <button class="page-link" onclick="loadPage(${
                         currentPage + 1
                       })">Next</button>
                   </li>`;
  paginationUl.innerHTML += nextLi;
}

document.addEventListener("DOMContentLoaded", function () {
  loadPage(1); // Load the first page initially
});
