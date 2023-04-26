const button = document.createElement("button");
button.innerText = "Download App";
button.style.backgroundColor = "blue";
button.style.color = "white";
button.style.border = "none";
button.style.marginBottom = "10px";
button.style.borderRadius = "6px";
button.style.padding = "10px";
button.style.fontSize = "12px";
button.style.display = "block";
button.style.margin = "0 auto";

button.addEventListener("click", () => {
    if (("standalone" in window.navigator) && window.navigator.standalone) {
        // The website is already added to the home screen
    } else {
        // The website is not yet added to the home screen
        const message = "Adicione esse aplicativo na tela inicial do celular.";
        const downloadButton = document.createElement("button");
        downloadButton.innerText = "Download App";
        downloadButton.addEventListener("click", () => {
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
                alert("O aplicativo foi adicionado na sua tela inicial com sucesso.");
            } else if (window.navigator.userAgent.match(/(Android)/i)) {
                // Add the shortcut to the home screen on Android
                const element = document.createElement("link");
                element.setAttribute("rel", "shortcut icon");
                element.setAttribute("type", "image/png");
                element.setAttribute("href", icon);
                document.head.appendChild(element);
                alert("O aplicativo foi adicionado na sua tela inicial com sucesso.");
            } else {
                // Prompt the user to manually add the shortcut to their home screen
                alert(message);
            }
        });
        document.body.appendChild(downloadButton);
        downloadButton.click();
        // Don't remove the button from the document here
    }
});

document.body.appendChild(button);
