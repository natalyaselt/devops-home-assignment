from fastapi import FastAPI
import uvicorn

from app.routes import router
from app.config import CONFIG
from app.logger import get_logger
from app.exceptions import register_exception_handlers

logger = get_logger(__name__)

# Create the FastAPI application.
app = FastAPI(title="Epoch Service")

# Use exception handler
register_exception_handlers(app)

# Register all REST endpoints.
app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok"}

# Start the application when this module is executed directly.
if __name__ == "__main__":
    """
    Entry point for running the service locally.
    Use configuration file for host and port.
    Set reload=True during development to automatically restart the server
    when source files change.
    """
    logger.info("Starting Epoch Service...")
    uvicorn.run(
        app,
        host=CONFIG["server"]["host"],
        port=CONFIG["server"]["port"],
        reload=False,
    )
