import json
import logging
import traceback
import typing as tp

import orjson
import sentry_sdk
from service.config import settings
from service.core.errors.errors import AppException
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError, PyJWTError
from pydantic import BaseModel, ValidationError
from starlette import status
from starlette.exceptions import HTTPException


def log_error(exc: Exception, request: Request) -> None:
    if settings.ENVIRONMENT in ["development", "local"]:
        route_handler = request.scope.get("route")
        handler_name = getattr(route_handler.endpoint, "__name__", "unknown") if route_handler else "unknown"
        module_name = getattr(route_handler.endpoint, "__module__", "unknown") if route_handler else "unknown"

        error_details = []
        if hasattr(exc, 'errors') and callable(getattr(exc, 'errors')):
            for err in exc.errors():
                loc = " -> ".join(str(loc_item) for loc_item in err.get("loc", []))
                error_details.append(
                    f"Error in {loc}: {err.get('msg')} (type: {err.get('type')}, input: {err.get('input', 'N/A')})")

        # Log request body for debugging
        body_details = ""
        if hasattr(request, '_body'):
            try:
                body_details = f"\nRequest body: {request._body.decode('utf-8')[:500]}"
            except Exception:
                body_details = "\nRequest body: <unable to decode>"

        error_message = f"Validation error for endpoint {request.url.path}\n"
        error_message += f"Handler: {module_name}.{handler_name}\n"
        error_message += "\n".join(error_details)
        error_message += body_details

        logging.error(error_message)
        logging.error(traceback.format_exc())


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Sequence[tp.Any]] = None


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, obj: tp.Any) -> tp.Any:
        if isinstance(obj, BaseModel):
            return obj.model_dump()

        try:
            orjson.dumps(obj)
        except TypeError:
            return str(obj)
        return super().default(obj)


class DataclassJSONResponse(JSONResponse):
    media_type = "application/json"

    def render(self, content: tp.Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
            cls=EnhancedJSONEncoder,
        ).encode("utf-8")


def create_response(
        status_code: int,
        data: tp.Optional[tp.Any] = None,
        errors: tp.Optional[tp.List[Error]] = None,
) -> JSONResponse:
    content = {}
    if data is not None:
        content["data"] = data

    if errors is not None:
        content["errors"] = errors

    return DataclassJSONResponse(status_code=status_code, content=content)


def server_error(errors: tp.List[Error]) -> JSONResponse:
    return create_response(status.HTTP_500_INTERNAL_SERVER_ERROR, errors=errors)


async def default_error_handler(request: Request, exc: Exception) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    log_error(exc, request)
    error = Error(
        error_key="server_error", error_message="Internal Server Error"
    )
    return server_error([error])


async def http_exception_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    log_error(exc, request)
    error = Error(error_key="http_exception", error_message=exc.detail)
    return create_response(status_code=exc.status_code, errors=[error])


async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    log_error(exc, request)
    error = Error(error_key="value_error", error_message=str(exc))
    return server_error([error])


async def validation_exception_handler(
        request: Request,
        exc: tp.Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    log_error(exc, request)
    errors = [
        Error(
            error_key=err.get("type"),  # type: ignore[arg-type]
            error_message=err.get("msg"),  # type: ignore[arg-type]
            error_loc=err.get("loc"),  # type: ignore[arg-type]
        )
        for err in exc.errors()
    ]
    return create_response(status.HTTP_422_UNPROCESSABLE_ENTITY, errors=errors)


async def jwt_expired_exception_handler(request: Request, exc: ExpiredSignatureError) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    errors = [
        Error(
            error_key="authorization.expired",
            error_message="Token has been expired",
            error_loc=["header", "Authorization"],
        )
    ]
    return create_response(status.HTTP_401_UNAUTHORIZED, errors=errors)


async def jwt_invalid_exception_handler(request: Request, exc: PyJWTError) -> JSONResponse:
    sentry_sdk.capture_exception(exc)
    errors = [
        Error(
            error_key="authorization.invalid",
            error_message="Token is invalid",
            error_loc=["header", "Authorization"],
        )
    ]
    return create_response(status.HTTP_401_UNAUTHORIZED, errors=errors)

async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    if exc.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR:
        sentry_sdk.capture_exception(exc)
    log_error(exc, request)
    errors = [
        Error(
            error_key=exc.error_key,
            error_message=exc.error_message,
            error_loc=exc.error_loc,
        )
    ]
    return create_response(exc.status_code, errors=errors)


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(ValueError, value_error_handler)  # type: ignore
    app.add_exception_handler(HTTPException, http_exception_error_handler)  # type: ignore
    app.add_exception_handler(ValidationError, validation_exception_handler)  # type: ignore
    app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore
    # service.add_exception_handler(ExpiredSignatureError, jwt_expired_exception_handler)
    # service.add_exception_handler(PyJWTError, jwt_invalid_exception_handler)
    app.add_exception_handler(AppException, app_exception_handler)  # type: ignore
    app.add_exception_handler(Exception, default_error_handler)  # type: ignore
