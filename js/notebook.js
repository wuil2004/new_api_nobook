document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll("div.jp-Notebook .input");
    cells.forEach(cell => {
        const button = document.createElement("button");
        button.innerText = "Mostrar/Ocultar código";
        button.style.marginBottom = "10px";
        button.addEventListener("click", () => {
            const codeBlock = cell.querySelector("pre");
            if (codeBlock.style.display === "none") {
                codeBlock.style.display = "block";
            } else {
                codeBlock.style.display = "none";
            }
        });
        cell.parentNode.insertBefore(button, cell);
    });
});
