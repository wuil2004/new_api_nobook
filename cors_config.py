from fastapi.middleware.cors import CORSMiddleware

def add_cors_middleware(app):
    """Configura el middleware de CORS para la aplicación."""
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Permite todas las conexiones de cualquier origen
        allow_credentials=True,
        allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
        allow_headers=["*"],  # Permite todos los encabezados
    )