import uvicorn
from fastapi import FastAPI

from api import endpoints
from config import settings
from services.logging_service import LoggingService

LoggingService.setup_logging()
app = FastAPI()
app.include_router(endpoints.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.server_port)
