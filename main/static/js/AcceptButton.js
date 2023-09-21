document.addEventListener("DOMContentLoaded", function() {
  const checkbox = document.getElementById("agree-checkbox");
  const signupButton = document.getElementById("signup-button");

  checkbox.addEventListener("change", function() {
    signupButton.disabled = !this.checked;
  });
});





