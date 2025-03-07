"""Main module for running application."""

from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_fastapi_instrumentator import Instrumentator

from src.config import app_config
from src.exceptions import ApplicationException
from src.logger import logger
from src.router.predict import router as predict_router
from src.utils.amenity import load_amenities_data
from src.utils.models import load_model


@asynccontextmanager
async def lifespan(application: FastAPI) -> AsyncIterator[None]:
    """Execute startup actions.
    
    Parameters
    ----------
     application: FastAPI
    
    Returns
    -------
     nothing
    
    """
    application.state.model = load_model(app_config)
    logger.info("Loaded model from mlflow")
    application.state.amenities_data = load_amenities_data(app_config.AMENITY_DIR_PATH)
    logger.info("Loaded amenities data from static dir")
    yield

app = FastAPI(
    lifespan=lifespan,
    title="Model Serving",
    description="This service allows to predict the price of an apartment in the city of Moscow",
)
app.include_router(predict_router, prefix="/api")
Instrumentator().instrument(app).expose(app, tags=["monitoring"])


@app.exception_handler(ApplicationException)
async def unicorn_exception_handler(request: Request, exc: ApplicationException) -> Response:
    """Handle applications errors.

    Parameters
    ----------
     request: Request
     exc: ApplicationException
    
    Returns
    -------
     Response
    
    """
    logger.error(f"{request.method} {request.url.path} {exc.status}, {exc.message}")
    return JSONResponse(
        status_code=exc.status,
        content={"message": exc.message},
    )
    

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, port=8000)