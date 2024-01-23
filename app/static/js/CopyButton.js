function copyText(token) {
  navigator.clipboard.writeText(token)
    .then(() => {
      console.log('Text copied to clipboard:', token);
    })
    .catch((error) => {
      console.error('Error copying text to clipboard:', error);
    });
}

