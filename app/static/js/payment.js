// TPDirect.setupSDK(
//   148927,
//   "app_pqn8isDobHevEDlBS9023r4syqCC539nPabKGYIFHOfrKMXqDRBRpYggogeu",
//   "sandbox"
// );

TPDirect.setupSDK(
  152793,
  "app_Ukv6aF5xgLj1608i6IoKZxgdVSttSEvYWLCh25v248I7M7rAUTI1Lf4eVjrK",
  "sandbox"
);

const csrfToken = document
  .querySelector('meta[name="csrf-token"]')
  .getAttribute("content");

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
        const reservationId = document.getElementById("rsv_id").textContent;
        const reservationName = document.getElementById("rsv_name").textContent;
        const reservationEmail = document.getElementById("rsv_email").textContent;
        const reservationCar = document.getElementById("rsv_car").textContent;
        const reservationAmount = document.getElementById("rsv_amount").textContent;
        const url = "/api/tappaysdk/pay-by-prime";
        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
          },
          body: JSON.stringify({
            prime: result.card.prime,
            partner_key: "partner_GVQwt2gIZgnvl8Q4joIDNTOqwD4r7D99ZCcaf630kIqFqbyBbjGGaSyF",
              // "partner_KOO8dhjMg4V7bifJUKXcuDXiYW0lK78oFvICgoeREFyh6Hp31fuu306X",
            // merchant_id: "tppf_annachu0988_GP_POS_1",
            merchant_id: "phoenix719_CTBC",
            details: reservationCar,
            amount: parseInt(reservationAmount) + 1,
            cardholder: {
              // phone_number: "+886923456789",
              phone_number: "+886963079658",
              name: reservationName,
              email: reservationEmail,
              order_number: reservationId,
              // zip_code: "100",
              // address: "台北市天龍區芝麻街1號1樓",
            }
          }),
        })
          .then((response) => response.json())
          .then((data) => {
            if (data.status === 0) {
              console.log(data);
              alert("Payment successful!");
              console.log("Payment processed successfully", data.auth_code);
              updatePaymentStatusOnServer(reservationId, "Success", data.auth_code);
              window.location.href = "/profile/orders";
            } else {
              alert("Payment failed: " + data.msg);
              console.error("Payment processing failed:", data.status);
              updatePaymentStatusOnServer(reservationId, "Failed");
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


  function updatePaymentStatusOnServer(reservationId, status, auth_code) {
    const updateUrl = "/api/update-payment-status";
    fetch(updateUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        reservationId: reservationId,
        status: status,
        auth_code: auth_code,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Server updated with new payment status:", data);
      })
      .catch((error) => {
        console.error("Failed to update payment status on server:", error);
      });
  }