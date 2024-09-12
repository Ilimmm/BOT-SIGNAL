import uvicorn
from main import app  # Импортируйте ваше FastAPI приложение

if __name__ == "__main__":
    # Запуск FastAPI сервера
    uvicorn.run(app, host="0.0.0.0", port=8000)
