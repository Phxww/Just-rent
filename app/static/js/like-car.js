document.addEventListener("DOMContentLoaded", function () {
  const csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute("content");
  document
    .getElementById("cars-container")
    .addEventListener("click", function (event) {
      const target = event.target;
      if (target.classList.contains("like-icon")) {
        const carId = target.dataset.carId;
        //  拿到 data-* 屬性的元素
        const isLiked = target.dataset.liked === "true";
        const url = isLiked
          ? `/api/unlike_car/${carId}` // 如果 isLiked 為 true，使用取消喜歡的 API
          : `/api/like_car/${carId}`; // 如果 isLiked 為 false，使用喜歡的 API
        console.log(carId);

        fetch(url, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            // Include CSRF token header if CSRF protection is enabled
            "X-CSRFToken": csrfToken,
          },
        })
          .then((response) => response.json())
          .then((data) => {
            console.log(data);
            if (data.error) {
              alert(data.error);
            } else {
              alert(data.message);
              //   <i class="like-icon fas fa-heart ${car.isLiked ? 'liked' : ''}" data-liked="${car.isLiked}" data-car-id="${car.id}"></i>
              target.dataset.liked = !isLiked; //  當前值的相反值 (將 data-liked 屬性翻轉，才能再下一次點擊時能觸發變化)
              target.classList.toggle("liked", !isLiked);
              target.style.color = isLiked ? "gray" : "red";
            }
          })
          .catch((error) => console.error("Error:", error));
      }
    });
});

// document.addEventListener("DOMContentLoaded", function () {
//   const csrfToken = document
//     .querySelector('meta[name="csrf-token"]')
//     .getAttribute("content");
//   document
//     .getElementById("cars-container")
//     .addEventListener("click", function (event) {
//       const target = event.target;
//       if (target.classList.contains("like-icon")) {
//         const carId = target.dataset.carId;
//         const isLiked = target.dataset.liked === "true";
//         const url = isLiked
//           ? `/api/unlike_car/${carId}`
//           : `/api/like_car/${carId}`;
//         console.log(carId);

//         fetch(url, {
//           method: "POST",
//           headers: {
//             "Content-Type": "application/json",
//             // Include CSRF token header if CSRF protection is enabled
//             "X-CSRFToken": csrfToken,
//           },
//         })
//           .then((response) => response.json())
//           .then((data) => {
//             if (data.error) {
//               alert(data.error);
//             } else {
//               alert(data.message);
//               // Update the UI accordingly
//             }
//           })
//           .catch((error) => console.error("Error:", error));
//       }
//     });
// });
