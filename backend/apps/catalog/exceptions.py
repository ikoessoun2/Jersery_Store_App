
from rest_framework.exceptions import APIException


class ApplicationException(APIException):
    status_code = 400
    default_detail = "An application error occurred."
    default_code = "application_error"


class ResourceNotFoundException(ApplicationException):
    status_code = 404
    default_detail = "The requested resource was not found."
    default_code = "resource_not_found"


class ResourceConflictException(ApplicationException):
    status_code = 409
    default_detail = "The resource already exists."
    default_code = "resource_conflict"