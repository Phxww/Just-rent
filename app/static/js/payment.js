// TPDirect.setupSDK(appID, appKey, serverType)
const APP_ID = "148927";
const APP_KEY =
  "app_pqn8isDobHevEDlBS9023r4syqCC539nPabKGYIFHOfrKMXqDRBRpYggogeu";

//  金鑰初始化
TPDirect.setupSDK(APP_ID, APP_KEY, "sandbox");

// 觸發送出表單
function onSubmit() {
  TPDirect.card.setup({
    fields: {
      number: {
        // The CSS selector of your card number input field
        element: "#card-number",
        placeholder: "**** **** **** ****",
      },
      expirationDate: {
        // The CSS selector of your card expiration date input field
        element: "#card-expiration-date",
        placeholder: "MM / YY",
      },
      ccv: {
        // The CSS selector of your card ccv input field
        element: "#card-ccv",
        placeholder: "ccv",
      },
    },
    styles: {
      // Add styles to your input fields if necessary
      input: {
        color: "gray",
      },
      ":focus": {
        color: "black",
      },
    },
  });

  // Get prime
  TPDirect.card.getPrime((result) => {
    if (result.status !== 0) {
      alert("Get prime error: " + result.msg);
      return;
    }
    alert("Get prime success, prime: " + result.card.prime);
    console.log("Prime token: ", result.card.prime);
  });
}
