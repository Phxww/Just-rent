document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/reservations")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((reservations) => {
      // Assuming the reservations variable contains an array of reservation data
      const tableBody = document.querySelector(".table tbody");
      reservations.forEach((reservation) => {
        const row = document.createElement("tr");
        row.innerHTML = `
                <td>${reservation.id}</td>
                <td>${reservation.car_name}</td>
                <td>${reservation.pick_up_location}</td>
                <td>${reservation.drop_off_location}</td>
                <td>${reservation.pick_up_date}</td>
                <td>${reservation.return_date}</td>
                <td>${getStatusBadge(reservation.status, reservation.id)}</td>
                </td>
            `;
        tableBody.appendChild(row);
      });
    })
    .catch((error) => {
      console.error("Failed to load reservations:", error);
      // Optionally update the UI to inform the user
    });
});
