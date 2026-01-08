"""
Punto de entrada para ejecutar la aplicación localmente.
Uso: python main.py
"""

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", port=8000, reload=True)
