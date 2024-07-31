"""Initialize insight-chat application."""

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.responses import Response

from app.api.routes.api_route import api_router
from app.core.config import config
from app.logger.logger import custom_logger


class LoggingMiddleware(BaseHTTPMiddleware):
    """Logging All API Requests"""

    async def dispatch(self, request, call_next: RequestResponseEndpoint) -> Response:
        custom_logger.info(
            f"Request: {request.method} {request.url} {request.client.host}"
        )
        response = await call_next(request)
        custom_logger.info("Response status code: %s", response.status_code)
        return response


def create_app() -> FastAPI:
    # Start the API
    app = FastAPI(title="Text Image Retrieval", version="0.1.0")

    custom_logger.debug("Setting up CORS middleware")
    app.add_middleware(
        CORSMiddleware,
        allow_credentials=True,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    custom_logger.debug("Setting up logging middleware")
    app.add_middleware(LoggingMiddleware)

    app.include_router(api_router, prefix="/api", tags=["Retrieval"])

    app.mount(
        "/app/frontend/static",
        app=StaticFiles(directory="app/frontend/static"),
        name="static",
    )

    templates = Jinja2Templates(directory="app/frontend/templates")

    @app.get("/", tags=["UI"])
    async def home(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.PORT, log_config=None)
