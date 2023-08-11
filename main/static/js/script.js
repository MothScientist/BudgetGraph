window.onload = function() {
  const gradientLine = document.getElementById("gradient-line");
  const colors = ["red", "yellow", "green", "blue"];
  let currentColorIndex = 0;

  function changeGradientColor() {
    gradientLine.style.background = `linear-gradient(to right, ${colors[currentColorIndex]}, ${colors[currentColorIndex + 1]})`;
    currentColorIndex = (currentColorIndex + 1) % (colors.length - 1);
  }

  setInterval(changeGradientColor, 750);
};