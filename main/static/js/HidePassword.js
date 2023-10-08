const closedImagePath = "static/img/hide.png";
const openedImagePath = "static/img/show.png";

function togglePasswordVisibility() {
  const passwordInput = document.getElementById("password");
  const passwordImage = document.getElementById("hide-image-password");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    passwordImage.src = openedImagePath;
  } else {
    passwordInput.type = "password";
    passwordImage.src = closedImagePath;
  }
}

function toggleTokenVisibility() {
  const tokenInput = document.getElementById("token");
  const tokenImage = document.getElementById("hide-image-token");

  if (tokenInput.type === "password") {
    tokenInput.type = "text";
    tokenImage.src = openedImagePath;
  } else {
    tokenInput.type = "password";
    tokenImage.src = closedImagePath;
  }
}


