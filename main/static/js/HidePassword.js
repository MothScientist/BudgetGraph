const closedImagePath = "static/img/hide.png";
const openedImagePath = "static/img/show.png";

function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  const passwordImage = document.getElementById("password-image");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordImage.src = openedImagePath;
  } else {
    passwordInput.type = "password";
    passwordImage.src = closedImagePath;
  }
}


