import logging

import yaml
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError, HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.exceptions.exception_handlers import ExceptionHandler
from app.exceptions.service_exception import ServiceException
from app.middlewares.request_middleware import RequestMiddleware
from app.routers import v1_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=False,
    allow_methods=['POST', 'GET'],
    allow_headers=['*'],
)

app.add_middleware(RequestMiddleware)
app.add_exception_handler(RequestValidationError, ExceptionHandler.validation_exception_handler)
app.add_exception_handler(HTTPException, ExceptionHandler.http_request_exception_handler)
app.add_exception_handler(ServiceException, ExceptionHandler.service_exception_handler)
app.add_exception_handler(Exception, ExceptionHandler.unhandled_exception_handler)

app.include_router(v1_router.router, prefix='/api')



@app.on_event('startup')
async def startup():
    with open('app/configs/log_config.yaml') as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
        logging.config.dictConfig(config)


@app.on_event('shutdown')
async def shutdown():
    pass