TPDirect.setupSDK(
  148927,
  "app_pqn8isDobHevEDlBS9023r4syqCC539nPabKGYIFHOfrKMXqDRBRpYggogeu",
  "sandbox"
);

TPDirect.card.setup("#tappay-iframe");
TPDirect.card.onUpdate(function (update) {
  if (update.canGetPrime) {
    document.getElementById("submit").disabled = false;
  } else {
    document.getElementById("submit").disabled = true;
  }
});

document
  .getElementById("payment-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    TPDirect.card.getPrime(function (result) {
      if (result.status === 0) {
        console.log("prime", result.card.prime);
        const reservationId = document.getElementById("reservation-id").value;
        fetch(`/api/get-reservation/${reservationId}`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            prime: result.card.prime,
            // Include other payment details if necessary
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.success) {
              alert("Payment successful!");
              console.log("Payment processed successfully");
            } else {
              alert("Payment failed: " + data.message);
              console.error("Payment processing failed:", data.error);
            }
          })
          .catch((error) => {
            console.error("Error sending prime to server:", error);
            alert("Error processing payment. Please try again.");
          });
      } else {
        console.error("Failed to get prime:", result.msg);
      }
    });
  });

