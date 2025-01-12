from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from cors_config import add_cors_middleware
import os
import nbformat
from nbconvert import HTMLExporter
from nbconvert.preprocessors import ExecutePreprocessor

app = FastAPI()

# Configuración de CORS
add_cors_middleware(app)

# Configuración de carpetas
UPLOAD_FOLDER = "notebooks"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Montar carpetas estáticas
app.mount("/css", StaticFiles(directory="css"), name="css")
app.mount("/js", StaticFiles(directory="js"), name="js")
app.mount("/notebooks", StaticFiles(directory=UPLOAD_FOLDER), name="notebooks")


@app.get("/", response_class=HTMLResponse)
def root():
    """Muestra la página principal."""
    try:
        with open("indx.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo indx.html no encontrado.")


@app.post("/upload/")
async def upload_notebook(file: UploadFile):
    """Sube un notebook y lo guarda en la carpeta de notebooks."""
    if not file.filename.endswith(".ipynb"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un notebook (.ipynb)")

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(filepath, "wb") as f:
        f.write(await file.read())

    return {"message": f"Notebook {file.filename} subido exitosamente."}


@app.get("/list/")
def list_notebooks():
    """Lista todos los notebooks disponibles."""
    files = os.listdir(UPLOAD_FOLDER)
    notebooks = [file for file in files if file.endswith(".ipynb")]
    return {"notebooks": notebooks}


@app.get("/notebook/{filename}/", response_class=HTMLResponse)
def view_notebook(filename: str, exclude_input: bool = False):
    """Convierte y muestra el contenido del notebook en formato HTML."""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    # Cargar el notebook
    with open(filepath, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Convertir a HTML usando nbconvert
    html_exporter = HTMLExporter()
    html_exporter.exclude_input = exclude_input
    html_content, _ = html_exporter.from_notebook_node(notebook)

    # Generar HTML con diseño
    html_content = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Notebook Viewer</title>
        <link rel="stylesheet" href="/css/notebook.css">
        <script src="/js/notebook.js"></script>
    </head>
    <body>
        <a href="/" class="back-button">Volver</a>
        <div class="container">
            <hr>
            <div class="notebook-content">
                {html_content}
            </div>
        </div>
    </body>
    </html>
    """

    return HTMLResponse(content=html_content)


@app.post("/execute/{filename}/")
def execute_notebook(filename: str):
    """Ejecuta las celdas del notebook y devuelve los resultados."""
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Notebook no encontrado")

    # Cargar el notebook
    with open(filepath, "r", encoding="utf-8") as f:
        notebook = nbformat.read(f, as_version=4)

    # Crear un preprocesador para ejecutar las celdas
    executor = ExecutePreprocessor(timeout=600, kernel_name="python3")
    try:
        executor.preprocess(notebook, {"metadata": {"path": UPLOAD_FOLDER}})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al ejecutar el notebook: {str(e)}")

    # Guardar el notebook ejecutado (opcional)
    executed_filepath = os.path.join(UPLOAD_FOLDER, f"executed_{filename}")
    with open(executed_filepath, "w", encoding="utf-8") as f:
        nbformat.write(notebook, f)

    # Devolver el resultado como JSON
    output_data = []
    for cell in notebook.cells:
        if cell.cell_type == "code":
            output_data.append({
                "cell": cell.source,
                "output": cell.get("outputs", [])
            })

    return JSONResponse(content={"executed": executed_filepath, "outputs": output_data})
