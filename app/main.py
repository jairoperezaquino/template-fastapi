from fastapi import FastAPI

import logging
from app import logger
from starlette.middleware.base import BaseHTTPMiddleware


app = FastAPI(on_startup=[logger.setup])
app.add_middleware(BaseHTTPMiddleware, dispatch=logger.setup_trace_id)

@app.get("/")
async def root():
    logging.info("Heythere!")
    return "OK"