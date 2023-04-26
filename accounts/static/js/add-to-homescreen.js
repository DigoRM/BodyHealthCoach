
if (("standalone" in window.navigator) && window.navigator.standalone) {
    // The website is already added to the home screen
  } else {
    // The website is not yet added to the home screen
    const message = "Add this website to your home screen for easier access.";
    const button = document.createElement("button");
    button.innerText = "Add to Home Screen";
    button.addEventListener("click", () => {
      // Prompt the user to add the shortcut to their home screen
      const icon = "/static/images/sennalogo.png";
      const title = "SennaTeam";
      const url = window.location.href;
      if (window.navigator.userAgent.match(/(iPhone|iPod|iPad)/i)) {
        // Add the shortcut to the home screen on iOS
        const element = document.createElement("link");
        element.setAttribute("rel", "apple-touch-icon");
        element.setAttribute("href", icon);
        element.setAttribute("title", title);
        document.head.appendChild(element);
        window.setTimeout(() => {
          alert("The website has been added to your home screen.");
        }, 500);
      } else if (window.navigator.userAgent.match(/(Android)/i)) {
        // Add the shortcut to the home screen on Android
        const element = document.createElement("link");
        element.setAttribute("rel", "shortcut icon");
        element.setAttribute("type", "image/png");
        element.setAttribute("href", icon);
        document.head.appendChild(element);
        window.setTimeout(() => {
          alert("The website has been added to your home screen.");
        }, 500);
      } else {
        // Prompt the user to manually add the shortcut to their home screen
        alert(message);
      }
    });
    document.body.appendChild(button);
  }
  