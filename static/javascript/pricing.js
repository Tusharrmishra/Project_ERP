document.addEventListener("DOMContentLoaded", function () {
  var basicLink = document.querySelector(".card:nth-child(1) .btn1");
  var proLink = document.querySelector(".card:nth-child(2) .btn1");
  var businessLink = document.querySelector(".card:nth-child(3) .btn1");

  basicLink.addEventListener("click", function () {
    window.location.href = "../template/payment.html";
  });

  proLink.addEventListener("click", function () {
    window.location.href = "../template/payment.html";
  });

  businessLink.addEventListener("click", function () {
    window.location.href = "../template/payment.html";
  });
});
