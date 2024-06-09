from fastapi import FastAPI

import logging
from app.logging_config import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI()


@app.get("/")
async def root():
    logger.info("This is an INFO message")
    logger.warning("This is a WARNING message")
    logger.error("This is an ERROR message")
    logger.debug("This is a DEBUG message")
    return f"OK"