

document
  .getElementById("signup-form")
  .addEventListener("submit", function (event) {
    event.preventDefault();

    var name = document.getElementById("name").value;

    var email = document.getElementById("email").value;
    var user_password = document.getElementById("user_password").value;

    fetch("/signup", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        name: name,
        email: email,
        user_password: user_password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Success:", data);
      })
      .catch((error) => {
        console.error("Error:", error);
      });
    this.submit();
  });

setTimeout(() => {
  const flashMessage = document.getElementById("flash-message");
  if (flashMessage) {
    flashMessage.remove();
  }
}, 3000);
