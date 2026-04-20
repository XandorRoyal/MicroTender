from app.entrypoint import app
import uvicorn
from app.settings import Settings

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run("app.entrypoint:app", host="0.0.0.0", port=settings.PORT, reload=True)
