const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");

document
  .getElementById("bookingForm")
  .addEventListener("submit", function (event) {
    event.preventDefault(); // Prevent the form from submitting normally

    // Retrieve form data
    var pickUpLocation = document.getElementById("pickupLocation").value;
    var dropOffLocation = document.getElementById("dropoffLocation").value;
    var pickUpDate = document.getElementById("date-picker").value;
    var returnDate = document.getElementById("date-return").value;

    if (pickUpDate > returnDate) {
      alert("Pick-up date must not be later than the return date.");
      return; // Stop the form submission
    }

    // Call checkAvailability function
    checkAvailability(
      pickUpLocation,
      dropOffLocation,
      pickUpDate,
      returnDate,
      function (available) {
        if (available) {
          // If available, proceed to payment
          initiatePaymentProcess();
        } else {
          // Show message if not available
          alert(
            "Selected car is not available for the chosen dates. Please select different dates."
          );
        }
      }
    );
  });

function checkAvailability(pickUpLocation, dropOffLocation, pickUpDate, returnDate, callback) {
  const data = {
    pickUpLocation: pickUpLocation,
    dropOffLocation: dropOffLocation,
    pickUpDate: pickUpDate,
    returnDate: returnDate,
    carId: carId,
  };

  fetch("/api/check-availability", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken,
    },
    body: JSON.stringify(data),
  })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Failed to fetch");
      }
      return response.json();
    })
    .then((data) => callback(data.available))
    .catch((error) => {
      console.error("Error checking availability:", error);
      alert("Failed to check availability. Please try again.");
    });
}

function initiatePaymentProcess() {
  // Implement TapPay or another payment process integration here
  window.location.href = "/payment";
}
