$(document).ready(function () {
  $("login__form").submit(function (e) {
    e.preventDefault();
    var formData = $(this).serialize();
    $.ajax({
      type: "POST",
      url: "/login",
      data: formData,
      success: function (response) {
        alert(response.message);
        window.location.href = "/";
      },
      error: function (xhr, status, error) {
        var errorMessage = JSON.parse(xhr.responseText).error;
        alert(errorMessage);
        window.location.href = "/signup";
      },
    });
  });
});
