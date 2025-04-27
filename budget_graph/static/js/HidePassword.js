const closedImagePath = "static/img/hide.png";
const openedImagePath = "static/img/show.png";

function toggleVisibility(inputId, imageId) {
  const inputField = document.getElementById(inputId);
  const imageElement = document.getElementById(imageId);

  if (inputField.type === "password") {
    inputField.type = "text";
    imageElement.src = openedImagePath;
  } else {
    inputField.type = "password";
    imageElement.src = closedImagePath;
  }
}

