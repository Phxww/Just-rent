document.addEventListener("DOMContentLoaded", function () {
  const cars = [
    {
      name: "Jeep Renegade",
      image: "https://fakeimg.pl/100x100/",
      seats: "5",
      luggage: "2",
      type: "SUV",
      rate: "$265",
    },
    {
      name: "Jeep Renegade",
      image: "https://fakeimg.pl/100x100/",
      seats: "5",
      luggage: "2",
      type: "SUV",
      rate: "$265",
    },
    {
      name: "Jeep Renegade",
      image: "https://fakeimg.pl/100x100/",
      seats: "5",
      luggage: "2",
      type: "SUV",
      rate: "$265",
    },
    {
      name: "Jeep Renegade",
      image: "https://fakeimg.pl/100x100/",
      seats: "5",
      luggage: "2",
      type: "SUV",
      rate: "$265",
    },
    {
      name: "Jeep Renegade",
      image: "https://fakeimg.pl/100x100/",
      seats: "5",
      luggage: "2",
      type: "SUV",
      rate: "$265",
    },
    // Add more car objects here
  ];

  const carouselInner = document.getElementById("carousel-inner");

  function createCarouselItem(cars, isActive) {
    // <div class="carousel-item active"></div>
    const itemDiv = document.createElement("div");
    itemDiv.className = `carousel-item ${isActive ? "active" : ""} `;
    // <div class="row"></div>
    const rowDiv = document.createElement("div");
    rowDiv.className = "row";

    cars.forEach((car) => {
      const colDiv = document.createElement("div");
      colDiv.className = "col-lg-4 col-md-12 mb-4 mb-lg-0";
      colDiv.innerHTML = `
        <img src="${car.image}" class="img-fluid mb-2" alt="${car.name}">
        <div class="car-info">
        <h5>${car.name}</h5>
        <p><i class="fas fa-user"></i> ${car.seats} <i class="fas fa-suitcase"></i> ${car.luggage} <i class="fas fa-car"></i> ${car.type}</p>
        <p>Daily rate from <span>${car.rate}</span></p>
        <a href="car-single.html" class="btn btn-primary">Rent Now</a>
        </div>
      `;
      rowDiv.appendChild(colDiv);
        itemDiv.appendChild(rowDiv);
        carouselInner.appendChild(itemDiv);
    });

    // itemDiv.appendChild(rowDiv);
    // carouselInner.appendChild(itemDiv);
  }

  // Create groups of 3 cars for each carousel item
  for (let i = 0; i < cars.length; i += 3) {
    createCarouselItem(cars.slice(i, i + 3), i === 0);
  }
});
