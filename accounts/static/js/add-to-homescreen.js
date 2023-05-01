const addToHomeScreenButton = document.createElement('button');
addToHomeScreenButton.textContent = 'Add to Home Screen';
addToHomeScreenButton.addEventListener('click', () => {
  const isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
  const isAndroid = navigator.userAgent.toLowerCase().includes('android');
  if (isIOS) {
    alert('To add this website to your home screen:\n\n1. Tap the Share button in Safari.\n2. Tap "Add to Home Screen".\n3. Choose a name for the shortcut and tap "Add".');
  } else if (isAndroid) {
    alert('To add this website to your home screen:\n\n1. Tap the menu button and tap "Add to Home screen".\n2. Choose a name for the shortcut and tap "Add".');
  } else {
    alert('To add this website to your home screen, please follow the instructions for your device.');
  }
});
document.body.appendChild(addToHomeScreenButton);
