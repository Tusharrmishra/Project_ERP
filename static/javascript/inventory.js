function uploadExcel() {
  var fileInput = document.getElementById("excel-file");
  var file = fileInput.files[0];
  var formData = new FormData();
  formData.append("file", file);

  fetch("/upload_excel", {
    method: "POST",
    body: formData,
  })
    .then((response) => {
      if (response.ok) {
        return response.json();
      }
      throw new Error("Network response was not ok.");
    })
    .then((data) => {
      // Display data on the page
      displayData(data);
    })
    .catch((error) => {
      console.error("Error during file upload:", error);
    });
}

function displayData(data) {
  var dataTable = document.getElementById("data-table");
  dataTable.innerHTML = ""; // Clear previous data

  if (data.error) {
    // Display error message
    dataTable.innerHTML =
      '<tr><td colspan="3">Error: ' + data.error + "</td></tr>";
  } else {
    // Display data rows
    data.data.forEach((item) => {
      var row =
        "<tr><td>" +
        item.ID +
        "</td><td>" +
        item.Name +
        "</td><td>" +
        item.Price +
        "</td></tr>";
      dataTable.innerHTML += row;
    });
  }
}
