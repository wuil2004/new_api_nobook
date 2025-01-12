const API_BASE_URL = "https://notbook-api.onrender.com";

const API_BASE_URL = "http://127.0.0.1:8000"; // URL base de tu API*/


// Mostrar el nombre del archivo seleccionado
function displayFileName() {
    const fileInput = document.getElementById("file-input");
    const fileNameDisplay = document.getElementById("file-name");

    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = `Archivo seleccionado: ${fileInput.files[0].name}`;
        fileNameDisplay.style.color = "#2b2d42"; // Color opcional para destacar el nombre
    } else {
        fileNameDisplay.textContent = ""; // Limpia si no hay archivo
    }
}

// Subir un notebook
async function uploadNotebook() {
    const fileInput = document.getElementById("file-input");
    const uploadResponse = document.getElementById("upload-response");
    const file = fileInput.files[0];

    if (!file) {
        uploadResponse.textContent = "Por favor selecciona un archivo.";
        uploadResponse.style.color = "red";
        return;
    }

    uploadResponse.textContent = "Cargando...";
    uploadResponse.style.color = "blue";

    const formData = new FormData();
    formData.append("file", file);

    try {
        const response = await fetch(`${API_BASE_URL}/upload/`, {
            method: "POST",
            body: formData,
        });

        const result = await response.json();

        if (response.ok) {
            uploadResponse.textContent = result.message;
            uploadResponse.style.color = "green";
            fetchNotebooks(); // Actualiza la lista
        } else {
            uploadResponse.textContent = result.detail || "Error desconocido.";
            uploadResponse.style.color = "red";
        }
    } catch (error) {
        uploadResponse.textContent = `Error: ${error.message}`;
        uploadResponse.style.color = "red";
    }

    setTimeout(() => {
        uploadResponse.textContent = "";
    }, 5000);
}

// Listar notebooks
async function fetchNotebooks() {
    const notebooksGrid = document.getElementById("notebooks-grid");
    notebooksGrid.innerHTML = "Cargando...";

    try {
        const response = await fetch(`${API_BASE_URL}/list/`);
        const result = await response.json();

        notebooksGrid.innerHTML = "";

        result.notebooks.forEach((notebook) => {
            const card = document.createElement("div");
            card.className = "card";

            const icon = document.createElement("div");
            icon.className = "card-icon";
            icon.innerHTML = "📒";

            const title = document.createElement("div");
            title.className = "card-title";
            title.textContent = notebook;

            const buttonsContainer = document.createElement("div");
            buttonsContainer.className = "card-buttons";

            const viewButton = document.createElement("button");
            viewButton.textContent = "Código";
            viewButton.onclick = () =>
                window.open(`${API_BASE_URL}/notebook/${notebook}/?exclude_input=false`, "_blank");

            const resultsButton = document.createElement("button");
            resultsButton.textContent = "Resultados";
            resultsButton.onclick = () =>
                window.open(`${API_BASE_URL}/notebook/${notebook}/?exclude_input=true`, "_blank");

            buttonsContainer.appendChild(viewButton);
            buttonsContainer.appendChild(resultsButton);

            card.appendChild(icon);
            card.appendChild(title);
            card.appendChild(buttonsContainer);

            notebooksGrid.appendChild(card);
        });
    } catch (error) {
        notebooksGrid.innerHTML = `Error al cargar la lista: ${error.message}`;
    }
}

// Función para ocultar/mostrar la lista de notebooks
function toggleNotebooks() {
    const notebooksGrid = document.getElementById("notebooks-grid");
    const button = document.getElementById("btn-lista");

    if (notebooksGrid.style.display === "none") {
        fetchNotebooks();
        notebooksGrid.style.display = "grid";
        button.textContent = "Ocultar Lista";
    } else {
        notebooksGrid.style.display = "none";
        button.textContent = "Cargar Lista";
    }
}
