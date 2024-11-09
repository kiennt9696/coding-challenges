#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from flask import request, current_app, jsonify
from werkzeug.exceptions import HTTPException
from application.http_code import HTTP_STATUS_CODES
from application.error_code import HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN, \
    HTTP_404_NOT_FOUND, HTTP_405_METHOD_NOT_ALLOWED, HTTP_406_NOT_ACCEPTABLE, \
    HTTP_409_CONFLICT, HTTP_413_REQUEST_ENTITY_TOO_LARGE, \
    HTTP_415_UNSUPPORTED_MEDIA_TYPE, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_429_TOO_MANY_REQUESTS
import werkzeug.exceptions as default


def http_status_message(status_code):
    """Maps an HTTP status code to the textual status"""

    return HTTP_STATUS_CODES.get(status_code, '')


def get_error_message(data):
    """Using for extract log from marshmallow validation

    Args:
        data (dict): Dictionary contain marshmallow validation result

    Returns:
        str/unicode: Message

    Example data:
    {
        'messages': {
            'info': {
                'rule_name': ['test server endpoint is exsited.']
            }
        },
        'exc': ValidationError({
            'info': {
                'rule_name': ['test server endpoint is exsited.']
            }
        }, status_code = 422, headers = {})
    }
    """
    try:
        messages = data['messages']
        return json.dumps(messages)
    except Exception:
        return 'Validation error, re-check your data.'


def error_data(error_code, message):
    """Constructs a dictionary with status and message for returning in an
    error response"""

    error = {
        'code': error_code,
        'message': message
    }
    return error


class ErrorException(Exception):
    error_type = 'about:blank'
    error_code = 0
    status = 500
    title = 'Internal Server Error'
    detail = 'Server is at unexpected condition that prevented it from fulfilling the request'
    message_detail = ''
    instance = ''
    remap = None
    suberror_details = {}

    def __init__(self, params=None, payload=None, error_code=None, message=None):
        Exception.__init__(self)
        self.error_type = self.__class__.error_type
        self.error_code = self.__class__.error_code
        self.status = self.__class__.status
        self.title = self.__class__.title
        self.detail = self.__class__.detail
        self.params = params
        self.payload = payload
        self.message_detail = self.__class__.message_detail
        self.remap = self.__class__.remap

        if error_code is not None:
            self.error_code = error_code
            self.detail = self.suberror_details.get(error_code,
                                                    self.__class__.detail)

        if message is not None:
            self.message_detail = message

    def make_response(self):
        self.message = {
            'type': self.error_type,
            'error_code': self.error_code,
            'status': self.status,
            'title': self.title,
            'detail': self.detail,
            'message': self.message_detail,
            'instance': request.url
        }
        if self.params is not None:
            try:
                self.message['detail'] = self.message['detail'].format(p=self.params)
            except Exception:
                raise APIException()
        if self.remap is not None:
            _message = {}
            for k, v in self.remap.items():
                _message[k] = self.message[v]
            self.message = _message
        if self.payload is not None:
            self.message.update(self.payload)
        print('////////////')
        print(self.message)
        print(self.status)
        return (
            json.dumps(self.message),
            self.status,
            {'Content-Type': 'application/problem+json'}
        )


class APIException(Exception):

    """The base exception class for all exceptions this library raises."""

    status_code = 500
    http_status_code = HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, error_code=None, *args):
        if error_code in self.http_status_code:
            self.error_code = error_code
        else:
            self.error_code = self.status_code
        message = self.http_status_code.get(
            error_code, http_status_message(self.status_code))
        self.message = message.format(*args)

    @property
    def description(self):
        return error_data(self.error_code, self.message)


class BadRequest(ErrorException):
    """HTTP 400 - Bad request: you sent some malformed data."""
    error_code = default.BadRequest.code
    status = default.BadRequest.code
    title = default.BadRequest.__name__
    detail = default.BadRequest.description


class Unauthorized(ErrorException):

    """HTTP 401 - Unauthorized: bad credentials."""

    error_code = default.Unauthorized.code
    status = default.Unauthorized.code
    title = default.Unauthorized.__name__
    detail = default.Unauthorized.description


class Forbidden(ErrorException):

    """HTTP 403 - Forbidden: your credentials don't give you access to this resource."""

    error_code = default.Forbidden.code
    status = default.Forbidden.code
    title = default.Forbidden.__name__
    detail = default.Forbidden.description


class NotFound(APIException):

    """HTTP 404 - Not found."""

    status_code = 404
    http_status_code = HTTP_404_NOT_FOUND


class MethodNotAllowed(APIException):

    """HTTP 405 - Method Not Allowed."""

    status_code = 405
    http_status_code = HTTP_405_METHOD_NOT_ALLOWED


class NotAcceptable(APIException):

    """HTTP 406 - Not Acceptable."""

    status_code = 406
    http_status_code = HTTP_406_NOT_ACCEPTABLE


class Conflict(APIException):

    """HTTP 409 - Conflict."""

    status_code = 409
    http_status_code = HTTP_409_CONFLICT


class OverLimit(APIException):

    """HTTP 413 - Over limit: you're over the API limits for this time period."""

    status_code = 413
    http_status_code = HTTP_413_REQUEST_ENTITY_TOO_LARGE


class UnsupportedMediaType(APIException):

    """HTTP 415 - Unsupported Media Type: Unsupported media type in the request Content-Type header."""

    status_code = 415
    http_status_code = HTTP_415_UNSUPPORTED_MEDIA_TYPE


class UnprocessableEntity(APIException):

    """HTTP 429 - Unprocessable Entity: The request was well-formed but was unable to be followed due to semantic errors."""

    status_code = 422
    http_status_code = HTTP_422_UNPROCESSABLE_ENTITY


class RateLimit(APIException):

    """HTTP 429 - Rate limit: you've sent too many requests for this time period."""

    status_code = 429
    http_status_code = HTTP_429_TOO_MANY_REQUESTS


def api_error_handler(error):
    if isinstance(error, HTTPException):
        code = error.code
        if not isinstance(error.description, dict):
            if code == 422:
                data = getattr(error, 'data')
                error.description = error_data(code, get_error_message(data))
            else:
                error.description = error_data(code, http_status_message(code))
    elif isinstance(error, APIException):
        code = error.status_code
    elif isinstance(error, ErrorException):
        code = error.status
        description = error.make_response()
        description = json.loads(description[0])
        return jsonify(code=code, error_code=error.error_code, message=description['message'],
                       description=description['detail']), code
    else:
        code = 500
        error.description = error_data(code, http_status_message(code))
    msg = 'HTTP_STATUS_CODE_{0}: {1}'.format(code, error.description)
    if code != 404:
        current_app.logger.error(msg, exc_info=error)
    if code == 404:
        return jsonify(code=code, subCode=4041004, message='The requested URL was not found on the server.',
                       description='Resource was not found.'), code
    return jsonify(error=error.description), code


class InvalidParameter(BadRequest):
    title = 'Invalid parameter'

    suberror_details = {
        "4001001": "field {param} not exist"
    }


class InvalidToken(Unauthorized):
    title = 'Invalid Token'
    suberror_details = {}


class InternalServerError(ErrorException):
    """HTTP 500 - Internal Server Error"""
    error_code = default.InternalServerError.code
    status = default.InternalServerError.code
    title = default.InternalServerError.__name__
    detail = default.InternalServerError.description


class InvalidPermission(Forbidden):
    title = 'Invalid permission'

    suberror_details = {}
