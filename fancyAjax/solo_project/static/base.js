document.addEventListener("mousemove", function(event) {
    const spinElement = document.querySelector(".spin");
    const mouseX = event.clientX;
    const mouseY = event.clientY;
    spinElement.style.left = mouseX*.5 + "px";
    spinElement.style.top = mouseY*.5 + "px";
});