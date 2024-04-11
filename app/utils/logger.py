import logging

# Since this application does log in middleware for each request and response, here just disable uvicorn access log
uvicorn_access = logging.getLogger('uvicorn.access')
uvicorn_access.disabled = False

logger = logging.getLogger('uvicorn')
logger.setLevel(logging.getLevelName(logging.DEBUG))